import json
import time
from sched import scheduler
import threading
from typing import Callable

import redis

class RepeatingThread:
    def __init__(self, interval: float):
        self.scheduler = scheduler(time.time, time.sleep)
        self.client =
        self.interval = interval

    def pub_actions(self):
        self.scheduler.enter(self.interval, 0, self.pub_actions)

    def pub_thread(self):
        self.scheduler.enter(0, 0, self.pub_actions)
        self.scheduler.run()

    def __call__(self, *args, **kwargs):
        return self.pub_thread()


class CallbackThread:
    def __init__(self, callback: Callable, channel: str):
        self.callback = callback
        self.channel = channel
        self.client = redis.Redis(
            host=HOSTNAME,
            port=PORT
        )
        self.pubsub = self.client.pubsub(ignore_subscribe_messages=True)

        self.pubsub.subscribe(channel)

    def __call__(self, *args, **kwargs):



def run(callback: Callable, app_func: Callable):
    sub = CallbackThread(callback, )
    s_thread.start()
    p_thread.join()
    s_thread.join()
