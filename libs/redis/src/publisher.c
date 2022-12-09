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
#include "publisher.h"
#include "base.h"

typedef struct redis_pub_t
{
    RedisBase context;
} redis_pub_t;

RedisPub
redis_pub_create()
{
    RedisPub base = calloc(1, sizeof(redis_pub_t));
    base->context = redis_base_create();
    return base;
}

void redis_pub_destroy(RedisPub base)
{
    redis_base_destroy(base->context);
    free(base);
}

void
redis_publish(RedisPub base, const char * channel, char * message)
{
    static redis_cmd_t command;
    command.command = redis_string_concat("PUBLISH ", channel);
    command.params = message;
    command.callback = 0;
    redis_base_execute_command(base->context, &command);
    free(command.command);
}

void
redis_pub_attach(RedisPub base, EventBase eb)
{
    redis_base_attach(base->context, eb);
}
