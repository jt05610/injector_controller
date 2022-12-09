/**
  ******************************************************************************
  * @file   redis_subscriber.c
  * @author Jonathan Taylor
  * @date   12/6/22
  * @brief  DESCRIPTION
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2022 Jonathan Taylor.
  * All rights reserved.
  *
  ******************************************************************************
  */

#include <stdlib.h>
#include "redis/consumer.h"
#include "redis/base.h"

typedef struct redis_subscriber_t
{
    RedisBase context;
} redis_subscriber_t;

typedef struct redis_subscription_t
{
    char * channel;
    subscribe_callback_t callback;
} redis_subscription_t;

RedisSubscriber
redis_subscriber_create(struct event_base * eb)
{
    RedisSubscriber base = calloc(1, sizeof(redis_subscriber_t));
    base->context = redis_base_create(eb);
    return base;
}

void
redis_subscriber_destroy(RedisSubscriber base)
{
    redis_base_destroy(base->context);
    free(base);
}

RedisCommand
create_command(char * cmd, char * params, redis_callback_t cb)
{
    RedisCommand result = calloc(1, sizeof(redis_command_t));
    result->command  = cmd;
    result->params   = params;
    result->callback = cb;
    return result;
}

void destroy_command(RedisCommand command)
{
    free(command);
}

void
redis_subscribe(RedisSubscriber base, RedisSubscription subscription)
{
    RedisCommand command = create_command(
            "SUBSCRIBE", subscription->channel, subscription->callback);
    redis_base_execute_command(base->context, command);
    destroy_command(command);
}

void
redis_psubscribe(RedisSubscriber base, RedisSubscription subscription)
{
    RedisCommand command = create_command(
            "PSUBSCRIBE", subscription->channel, subscription->callback);
    redis_base_execute_command(base->context, command);
    destroy_command(command);
}

void
redis_unsubscribe(RedisSubscriber base, RedisSubscription subscription)
{
    RedisCommand command = create_command(
            "UNSUBSCRIBE", subscription->channel, subscription->callback);
    redis_base_execute_command(base->context, command);
    destroy_command(command);
}

RedisSubscription
redis_subscription_create(char * channel, subscribe_callback_t callback)
{
    RedisSubscription result = calloc(1, sizeof(redis_subscription_t));
    result->channel  = channel;
    result->callback = callback;
    return result;
}

void redis_subscription_destroy(RedisSubscription subscription)
{
    free(subscription);
}
