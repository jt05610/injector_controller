/**
  ******************************************************************************
  * @file   fixtures.cpp
  * @author Jonathan Taylor
  * @date   12/8/22
  * @brief  Test fixtures for redis
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2022 Jonathan Taylor.
  * All rights reserved.
  *
  ******************************************************************************
  */
#include "fixtures.h"
#include <event2/event.h>

static struct
{
    struct event * watchdog;
} self = {0};

static void
wd_cb(int fd, short event, void * arg)
{
    (void) fd;
    (void) event;
    (void) arg;
    struct event_base * b = (struct event_base *) arg;
    event_base_loopbreak(b);
}

EventBase
stoppable_event_base(int fd, int on)
{
    EventBase eb = event_base_new();
    self.watchdog = event_new(eb, fd, on, wd_cb, eb);
    event_add(self.watchdog, NULL);
    return eb;
}

void
stoppable_event_teardown(struct event_base * se)
{
    event_free(self.watchdog);
    event_base_free(se);
}

void
redis_publish_to_test(RedisBase base, char * msg, r_cb_t cb)
{

    redis_cmd_t cmd = {
            (char *) "PUBLISH test",
            msg,
            cb,

    };
    redis_base_execute_command(base, &cmd);
}