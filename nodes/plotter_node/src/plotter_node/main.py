import json
import time
from sched import scheduler
import threading

import redis

HOSTNAME = "127.0.0.1"
PORT = 6379


class RepeatingThread:
    def __init__(self, interval: float):
        self.scheduler = scheduler(time.time, time.sleep)
        self.client = redis.Redis(
            host=HOSTNAME,
            port=PORT
        )
        self.interval = interval

    def pub_actions(self):
        self.client.publish("modbus.coil.read.req", "1 0 1")
        self.client.publish("modbus.input_registers.read.req", "1 0 1")
        self.scheduler.enter(self.interval, 0, self.pub_actions)

    def pub_thread(self):
        self.scheduler.enter(0, 0, self.pub_actions)
        self.scheduler.run()

    def __call__(self, *args, **kwargs):
        return self.pub_thread(z1)


def sub_thread():
    r = redis.Redis(
        host=HOSTNAME,
        port=PORT
    )
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("modbus.coil.read.res", "modbus.input_registers.read.res")
    for m in pubsub.listen():
        data = json.loads(m["data"])
        if m["channel"] == b"modbus.input_registers.read.res":
            print("button_press", data)
        else:
            print("distance", data)


def main():
    pub = RepeatingThread(1)
    p_thread = threading.Thread(target=pub)
    s_thread = threading.Thread(target=sub_thread)
    p_thread.start()
    s_thread.start()
    p_thread.join()
    s_thread.join()


if __name__ == "__main__":
    main()
