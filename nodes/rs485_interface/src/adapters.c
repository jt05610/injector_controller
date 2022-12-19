/**
  ******************************************************************************
  * @file   adapters.c
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

#include <string.h>
#include <stdlib.h>
#include "adapters.h"
#include "redis_client.h"

ModbusRequest
redis_to_modbus(char * msg, mb_func_code_t func_code, modbus_callback_t callback, void * callback_struct)
{
    if(msg == NULL)
        return NULL;
    char * context;
    char * ptr;
    uint16_t values[3];
    char * token = strtok_r(msg, " ", &context);
    for(uint8_t i = 0; i < 3; i ++) {
        values[i] = strtol(token, &ptr, 10);
        token = strtok_r(NULL, " ", &context);
    }
    ModbusPDU pdu = mb_pdu_create(values[0], func_code, values[1], values[2], callback_struct);
    return modbus_request_create(pdu, callback);
}
