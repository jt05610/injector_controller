/**
  ******************************************************************************
  * @file   app.c
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

#include <stdlib.h>
#include "service_layer/app.h"
#include "service_layer/handlers.h"
#include "redis/redis_client.h"
#include "modbus/modbus_client.h"
#include "config.h"
#include "async.h"

typedef struct app_t {
    ModbusClient mb_client;
    RedisClient redis_client;
    RedisSubscription subs[6];
} app_t;


App
app_create()
{
    App ret = calloc(1, sizeof(app_t));
    signal(SIGPIPE, SIG_IGN);
    ret->redis_client = redis_client_create();
    ret->mb_client = modbus_client_create(ret->redis_client);
    return ret;
}

void
app_destroy(App app)
{
    for (uint8_t i = 0; i < 6; i ++)
        redis_subscription_destroy(app->subs[i]);
    redis_client_destroy(app->redis_client);
    modbus_client_destroy(app->mb_client);
    free(app);
}


static void
init_modbus(App app)
{
    modbus_client_connect(app->mb_client);
}

static App base;

void
hndl(
        __attribute__((unused)) redisAsyncContext * ctx, void * reply,
        void * privdata)
{
    redisReply *rep = (redisReply*)reply;
    if (rep == NULL)
        return;
    if (rep->str != NULL)
        redis_client_publish(base->redis_client, MB_READ_COIL_RES_CHANNEL, rep->str);
}


static void
init_redis(App app)
{
    base = app;

    static char * sub_channels[6] = {
            MB_READ_COIL_REQ_CHANNEL,
            MB_READ_DI_REQ_CHANNEL,
            MB_READ_HR_REQ_CHANNEL,
            MB_READ_IR_REQ_CHANNEL,
            MB_WRITE_COIL_REQ_CHANNEL,
            MB_WRITE_HR_REQ_CHANNEL,
    };

    static redis_callback_t redis_req_handlers[6] = {
            hndl,
handle_read_di,
            handle_read_hr,
            handle_read_ir,
            handle_write_coil,
            handle_write_hr,
    };

    for (uint8_t i = 0; i < 1; i ++) {
        app->subs[i] = redis_subscription_create(sub_channels[i], redis_req_handlers[i]);
        redis_client_subscribe(app->redis_client, app->subs[i]);
    }
}

void app_run(App app)
{
    init_modbus(app);
    init_redis(app);

}

