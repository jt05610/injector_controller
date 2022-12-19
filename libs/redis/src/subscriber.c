/**
  ******************************************************************************
  * @file   subscriber.c
  * @author Jonathan Taylor
  * @date   12/6/22
  * @brief  Registering and handling redis subscriptions
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2022 Jonathan Taylor.
  * All rights reserved.
  *
  ******************************************************************************
  */

#include <stdlib.h>
#include <stdbool.h>
#include "subscriber.h"
#include "base.h"

typedef struct redis_subscription_t * RedisSubscription;

typedef struct redis_sub_t
{
    RedisBase context;
    RedisSubscription * subs;
    size_t max_subs;
    size_t n_subs;

} redis_sub_t;

typedef struct redis_subscription_t
{
    char * channel;
    r_cb_t callback;

} redis_subscription_t;

static inline void execute_subs(RedisSub base, char * type, bool cb);

RedisSub
redis_sub_create(size_t max_subs)
{
    RedisSub base = calloc(1, sizeof(redis_sub_t));
    base->context  = redis_base_create();
    base->subs     = calloc(max_subs, sizeof(redis_subscription_t));
    base->max_subs = max_subs;
    base->n_subs   = 0;
    return base;
}

void
redis_sub_destroy(RedisSub base)
{
    for (size_t i = 0; i < base->n_subs; i++)
    {
        free(base->subs[i]);
    }
    redis_base_destroy(base->context);
    free(base);
}

void
redis_subscribe(RedisSub base)
{
    execute_subs(base, "SUBSCRIBE", true);
}

void
redis_unsubscribe(RedisSub base)
{
    execute_subs(base, "UNSUBSCRIBE", false);
}

void
redis_sub_add(RedisSub base, char * channel, r_cb_t callback)
{
    if (base->n_subs < base->max_subs)
    {
        base->subs[base->n_subs] = calloc(1, sizeof(redis_sub_t));
        base->subs[base->n_subs]->channel  = channel;
        base->subs[base->n_subs]->callback = callback;
        base->n_subs++;
    }
}

void
redis_sub_attach(RedisSub subscriber, EventBase eb)
{
    redis_base_attach(subscriber->context, eb);
}

static inline void
execute_subs(RedisSub base, char * type, bool cb)
{
    redis_cmd_t cmd;
    cmd.command = type;
    for (size_t i = 0; i < base->n_subs; i++)
    {
        cmd.params   = base->subs[i]->channel;
        cmd.callback = cb ? base->subs[i]->callback : 0;
        redis_base_execute_command(base->context, &cmd);
    }
}

void
redis_sub_set_data(RedisSub base, void * data)
{
    redis_base_set_data(base->context, data);
}
