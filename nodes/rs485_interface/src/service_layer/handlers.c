/**
  ******************************************************************************
  * @file   handlers.c
  * @author Jonathan Taylor
  * @date   12/7/22
  * @brief  DESCRIPTION
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2022 Jonathan Taylor.
  * All rights reserved.
  *
  ******************************************************************************
  */

#include <stdbool.h>
#include "service_layer/handlers.h"
#include "service_layer/adapters.h"
#include "service_layer/app.h"
#include "redis/redis_client.h"

typedef struct redis_cb_t * CB;

typedef struct redis_cb_t
{
    modbus_callback_t call;
    const char * channel;
    bool bit;
} redis_cb_t;

static void
_callback(const char * channel, bool bit, mb_result_t * result, void * privdata)
{
    char        msg[7];
    RedisClient client = (RedisClient) privdata;
    uint16_t    value;
    if (bit)
    {
        value = result->small[0];
    } else
    {
        value = result->big[0];
    }
    sprintf(msg, "%d", value);
    redis_client_publish(client, channel, msg);
}

static void
call(mb_result_t * result, void * callback, void * redis_client)
{
    CB cb = (CB) callback;
    _callback(cb->channel, cb->bit, result, redis_client);
}

void
handle(mb_func_code_t func_code, void * reply, void * privdata)
{
    static redis_cb_t callbacks[6] = {
            {call, MB_READ_COIL_RES_CHANNEL,  true},
            {call, MB_READ_DI_RES_CHANNEL,    true},
            {call, MB_READ_HR_RES_CHANNEL,    true},
            {call, MB_READ_IR_RES_CHANNEL,    true},
            {call, MB_WRITE_COIL_RES_CHANNEL, false},
            {call, MB_WRITE_HR_RES_CHANNEL,   false},
    };
    redisReply * rep = (redisReply *) reply;

    if (rep == NULL)
        return;
    if (rep->type != REDIS_REPLY_STRING)
    {
        return;
    }
    ModbusClient  client = (ModbusClient) privdata;
    ModbusRequest req    = redis_to_modbus(
            rep->str, func_code, callbacks[func_code - 1].call, &callbacks[func_code - 1]);
    modbus_client_request(client, req);
}

void
handle_read_coil(
        __attribute__((unused)) redisAsyncContext * ctx, void * reply,
        void * privdata)
{
    handle(MB_READ_COILS, reply, privdata);
}

void
handle_read_di(
        __attribute__((unused)) redisAsyncContext * ctx, void * reply,
        void * privdata)
{
    handle(MB_READ_DI, reply, privdata);
}

void
handle_read_hr(
        __attribute__((unused)) redisAsyncContext * ctx, void * reply,
        void * privdata)
{
    handle(MB_READ_HR, reply, privdata);
}

void
handle_read_ir(
        __attribute__((unused)) redisAsyncContext * ctx, void * reply,
        void * privdata)
{
    handle(MB_READ_IR, reply, privdata);
}

void
handle_write_coil(
        __attribute__((unused)) redisAsyncContext * ctx, void * reply,
        void * privdata)
{
    handle(MB_WRITE_COIL, reply, privdata);
}

void
handle_write_hr(
        __attribute__((unused)) redisAsyncContext * ctx, void * reply,
        void * privdata)
{
    handle(MB_WRITE_REGISTER, reply, privdata);
}