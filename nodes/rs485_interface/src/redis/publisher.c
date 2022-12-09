/**
  ******************************************************************************
  * @file   redis_publisher.c
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
#include "redis/publisher.h"
#include "redis/base.h"

typedef struct redis_publisher_t
{
    RedisBase context;
} redis_publisher_t;

RedisPublisher
redis_publisher_create(CFRunLoopRef loop)
{
    RedisPublisher base = calloc(1, sizeof(redis_publisher_t));
    base->context = redis_base_create(loop);
    return base;
}

void redis_publisher_destroy(RedisPublisher base)
{
    redis_base_destroy(base->context);
    free(base);
}

static void
publish_callback(redisAsyncContext * c, void * reply, void * privdata)
{
}

void redis_publish(RedisPublisher base, const char * channel, char * message)
{
    static redis_command_t command;
    command.command = redis_string_concat("PUBLISH ", channel);
    command.params = message;
    command.callback = publish_callback;
    redis_base_execute_command(base->context, &command);
    free(command.command);
}
