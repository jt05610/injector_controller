/**
  ******************************************************************************
  * @file   redis_base.c
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

#include "base.h"
#include "PROJECT_CONFIGURATION.h"
#include "hiredis.h"
#include <stdlib.h>
#include <string.h>
#include "adapters/libevent.h"

typedef enum redis_connection_state_t
{
    NOT_CONNECTED,
    CONNECTING,
    CONNECTED,
    DISCONNECTING,
} redis_connection_state_t;

typedef struct redis_base_t
{
    redisAsyncContext * context;
    redisReply        * reply;
    redisOptions             opt;
    redis_connection_state_t state;
    struct event_base * base;
    int err;
    void * data;
} redis_base_t;

void app_connect(const redisAsyncContext * c, int status);

void app_disconnect(const redisAsyncContext * c, int status);

RedisBase
redis_base_create()
{
    RedisBase base = calloc(1, sizeof(redis_base_t));
    base->state = CONNECTING;

    struct timeval tv = {0};
    tv.tv_sec = 1;
    REDIS_OPTIONS_SET_TCP(&base->opt, HOSTNAME, REDIS_PORT);
    base->opt.connect_timeout = &tv;

    base->context = redisAsyncConnectWithOptions(&base->opt);
    if (base->context->err)
    {
        printf("Error: %s\n", base->context->errstr);
        redisAsyncFree(base->context);
        base->context = NULL;
        base = NULL;
    } else
    {
        base->context->data = base;
        base->reply         = calloc(1, sizeof(redisReply));
    }
    return base;
}


void
redis_base_set_data(RedisBase base, void * data)
{
    base->context->data = data;
}

redisFD
redis_base_get_fd(RedisBase base)
{
    return base->context->c.fd;
}

void
redis_base_destroy(RedisBase base)
{
    base->state = DISCONNECTING;
    redisAsyncDisconnect(base->context);
}

void
app_connect(const redisAsyncContext * c, int status)
{
    RedisBase base = (RedisBase) c->data;

    if (status == REDIS_OK)
    {
        base->state = CONNECTED;
    } else
    {
        base->state = NOT_CONNECTED;
        base->err   = c->err;
    }
}

void
app_disconnect(const redisAsyncContext * c, int status)
{
    RedisBase base = (RedisBase) c->data;
    base->state = NOT_CONNECTED;
    base->err   = c->err;
    redis_base_destroy(base);
}

void
redis_base_execute_command(RedisBase base, RedisCommand command)
{
    static const char * format_base = " %s";

    char * format = redis_string_concat(command->command, format_base);
    redisAsyncCommand(
            base->context, command->callback, 0, format, command->params);
    free(format);
}

char * redis_string_concat(const char * first, const char * second)
{
    char * result = calloc(strlen(first) + strlen(second) + 1, sizeof(char));
    strcpy(result, first);
    strcat(result, second);
    return result;
}

redisAsyncContext *
redis_base_context(RedisBase base)
{
    return base->context;
}

void redis_base_attach(RedisBase base, struct event_base * eb)
{
    redisLibeventAttach(base->context, eb);
    redisAsyncSetConnectCallback(base->context, app_connect);
    redisAsyncSetDisconnectCallback(base->context, app_disconnect);
}

char *
extract_content(void * reply)
{
    char       * res = NULL;
    redisReply * rpl = (redisReply *) reply;
    if (rpl != NULL)
    {
        res = rpl->element[2]->str;
    }
    return res;
}
