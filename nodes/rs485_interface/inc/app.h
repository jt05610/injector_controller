/**
  ******************************************************************************
  * @file   app.h
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

#ifndef MODBUS_CLIENT_APP_H
#define MODBUS_CLIENT_APP_H

#include "modbus_client.h"
#include "redis_client.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct app_t * App;


typedef struct app_t
{
    ModbusClient mb_client;
    RedisClient  redis_client;
} app_t;

App app_create();

void app_destroy(App app);

void app_run(App app);

void app_init(App app);

void app_spin_once(App app);

#ifdef __cplusplus
}
#endif

#endif //MODBUS_CLIENT_APP_H
