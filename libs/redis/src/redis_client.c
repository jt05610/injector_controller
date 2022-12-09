/**
  ******************************************************************************
  * @file   redis_client.c
  * @author Jonathan Taylor
  * @date   12/6/22
  * @brief  Code for configuring and running asynchronous redis client.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2022 Jonathan Taylor.
  * All rights reserved.
  *
  ******************************************************************************
  */

#include <stdlib.h>
#include "redis_client.h"
#include "publisher.h"
#include "subscriber.h"

typedef struct redis_client_t
{
    RedisPub  publisher;
    RedisSub  subscriber;
    EventBase eb;
} redis_client_t;

RedisClient
redis_client_create(size_t n_subs)
{
    RedisClient base = calloc(1, sizeof(redis_client_t));
    base->publisher  = redis_pub_create();
    base->subscriber = redis_sub_create(n_subs);
    base->eb         = event_base_new();
    return base;
}

void
redis_client_destroy(RedisClient base)
{
    redis_pub_destroy(base->publisher);
    redis_sub_destroy(base->subscriber);
    event_base_free(base->eb);
    free(base);
}

void
redis_client_publish(RedisClient base, const char * channel, char * message)
{
    redis_publish(base->publisher, channel, message);
}

void
redis_client_subscribe(RedisClient base)
{
    redis_subscribe(base->subscriber);

}

void
redis_client_new_sub(RedisClient base, char * channel, r_cb_t callback)
{
    redis_sub_add(base->subscriber, channel, callback);
}

void
redis_client_run(RedisClient base)
{
    redis_client_attach(base);
    redis_subscribe(base->subscriber);
    event_base_dispatch(base->eb);
}

void
redis_client_attach(RedisClient base)
{
    redis_sub_attach(base->subscriber, base->eb);
    redis_pub_attach(base->publisher, base->eb);

}

void
redis_client_spin_once(RedisClient base)
{
    event_base_loop(base->eb, EVLOOP_NONBLOCK);
}