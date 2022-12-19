/**
  ******************************************************************************
  * @file   redis_base.h
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

#ifndef MODBUS_CLIENT_BASE_H
#define MODBUS_CLIENT_BASE_H


#ifdef __cplusplus
extern "C" {
#endif

#include "async.h"

typedef struct event_base * EventBase;

typedef struct redis_base_t * RedisBase;

typedef struct redis_cmd_t * RedisCommand;

typedef void (* r_cb_t)(redisAsyncContext * c, void * reply, void * privdata);

typedef struct redis_cmd_t
{
    char * command;
    char * params;
    r_cb_t callback;

} redis_cmd_t;

RedisBase redis_base_create();

void redis_base_destroy(RedisBase base);

void redis_base_attach(RedisBase base, EventBase eb);

void redis_base_execute_command(RedisBase base, RedisCommand command);

char * redis_string_concat(const char * first, const char * second);

redisFD redis_base_get_fd(RedisBase base);

char * extract_content(void * reply);

void redis_base_set_data(RedisBase base, void * data);

#ifdef __cplusplus
}
#endif

#endif //MODBUS_CLIENT_BASE_H
