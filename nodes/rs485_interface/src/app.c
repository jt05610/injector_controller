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
#include "app.h"
#include "handlers.h"
#include "redis_client.h"
#include "modbus_client.h"
#include "config.h"

App
app_create()
{
    App ret = calloc(1, sizeof(app_t));
    signal(SIGPIPE, SIG_IGN);
    ret->redis_client = redis_client_create(N_SUB_CHANNELS);
    ret->mb_client    = modbus_client_create(ret->redis_client);
    redis_client_set_data(ret->redis_client, ret);
    return ret;
}

void
app_destroy(App app)
{
    redis_client_destroy(app->redis_client);
    modbus_client_destroy(app->mb_client);
    free(app);
}

static void
init_modbus(App app)
{
    modbus_client_connect(app->mb_client);
}

static inline void
_handle(redisAsyncContext * ctx, void * reply, void * privdata)
{
    App base = (App)ctx->data;

    redisReply * rep = (redisReply *) reply;
    if (rep == NULL)
    {
        return;
    }
    if (rep->str != NULL)
    {
        redis_client_publish(base->redis_client, MB_READ_COIL_RES_CHANNEL, rep->str);
    }
}


static void
init_redis(App app)
{

    static char * sub_channels[N_SUB_CHANNELS] = {
            MB_READ_COIL_REQ_CHANNEL,
            MB_READ_DI_REQ_CHANNEL,
            MB_READ_HR_REQ_CHANNEL,
            MB_READ_IR_REQ_CHANNEL,
            MB_WRITE_COIL_REQ_CHANNEL,
            MB_WRITE_HR_REQ_CHANNEL,
    };

    static r_cb_t redis_req_handlers[N_SUB_CHANNELS] = {
            handle_read_coil,
            handle_read_di,
            handle_read_hr,
            handle_read_ir,
            handle_write_coil,
            handle_write_hr,
    };
    for (size_t i = 0; i < N_SUB_CHANNELS; i ++)
        redis_client_new_sub(app->redis_client, sub_channels[i], redis_req_handlers[i]);
    redis_client_attach(app->redis_client);
    redis_client_subscribe(app->redis_client);
}

void
app_init(App app)
{

    init_modbus(app);
    init_redis(app);
}

void
app_run(App app)
{
    redis_client_run(app->redis_client);
}

void
app_spin_once(App app)
{
    redis_client_spin_once(app->redis_client);
}

