/**
  ******************************************************************************
  * @file   handlers.h
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

#ifndef MODBUS_CLIENT_HANDLERS_H
#define MODBUS_CLIENT_HANDLERS_H
#ifdef __cplusplus
extern "C" {
#endif

#include "async.h"
#include "../../../libs/redis/inc/base.h"

void handle_read_coil(__attribute__((unused)) redisAsyncContext * ctx, void * reply, void * privdata);

void handle_read_di(redisAsyncContext * ctx, void * reply, void * privdata);

void handle_read_hr(redisAsyncContext * ctx, void * reply, void * privdata);

void handle_read_ir(redisAsyncContext * ctx, void * reply, void * privdata);

void handle_write_coil(redisAsyncContext * ctx, void * reply, void * privdata);

void handle_write_hr(redisAsyncContext * ctx, void * reply, void * privdata);

#ifdef __cplusplus
}
#endif

#endif //MODBUS_CLIENT_HANDLERS_H
