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
#include "handlers.h"
#include "adapters.h"
#include "config.h"
#include "app.h"

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
handle(mb_func_code_t func_code, redisAsyncContext * ctx, void * reply)
{
    App base = (App)ctx->data;
    static redis_cb_t callbacks[6] = {
            {call, MB_READ_COIL_RES_CHANNEL,  true},
            {call, MB_READ_DI_RES_CHANNEL,    true},
            {call, MB_READ_HR_RES_CHANNEL,    true},
            {call, MB_READ_IR_RES_CHANNEL,    true},
            {call, MB_WRITE_COIL_RES_CHANNEL, false},
            {call, MB_WRITE_HR_RES_CHANNEL,   false},
    };
    char * msg = extract_content(reply);
    if (msg != NULL) {
        ModbusRequest req    = redis_to_modbus(
                msg, func_code, callbacks[func_code - 1].call, &callbacks[func_code - 1]);
        modbus_client_request(base->mb_client, req);
    }
}

void
handle_read_coil(redisAsyncContext * ctx, void * reply, void * privdata)
{
    (void) privdata;
    handle(MB_READ_COILS, ctx, reply);
}

void
handle_read_di(redisAsyncContext * ctx, void * reply, void * privdata)
{
    (void) privdata;
    handle(MB_READ_DI, ctx, reply);
}

void
handle_read_hr(redisAsyncContext * ctx, void * reply, void * privdata)
{
    (void) privdata;
    handle(MB_READ_HR, ctx, reply);
}

void
handle_read_ir(redisAsyncContext * ctx, void * reply, void * privdata)
{
    (void) privdata;
    handle(MB_READ_IR, ctx, reply);
}

void
handle_write_coil(redisAsyncContext * ctx, void * reply, void * privdata)
{
    (void) privdata;
    handle(MB_WRITE_COIL, ctx, reply);
}

void
handle_write_hr(redisAsyncContext * ctx, void * reply, void * privdata)
{
    (void) privdata;
    handle(MB_WRITE_REGISTER, ctx, reply);
}
