/**
  ******************************************************************************
  * @file   adapters.h
  * @author Jonathan Taylor
  * @date   12/8/22
  * @brief  DESCRIPTION
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2022 Jonathan Taylor.
  * All rights reserved.
  *
  ******************************************************************************
  */

#ifndef MODBUS_CLIENT_ADAPTERS_H
#define MODBUS_CLIENT_ADAPTERS_H

#include "../../../libs/redis/inc/redis_client.h"

#ifdef __cplusplus
extern "C" {
#endif

#include "../../../libs/modbus/inc/modbus_client.h"
#include "async.h"

ModbusRequest redis_to_modbus(char * msg, mb_func_code_t func_code, modbus_callback_t callback, void * callback_struct);

#ifdef __cplusplus
}
#endif


#endif //MODBUS_CLIENT_ADAPTERS_H
