/**
  ******************************************************************************
  * @file   config.h
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

#ifndef MODBUS_CLIENT_CONFIG_H
#define MODBUS_CLIENT_CONFIG_H

#ifdef __cplusplus
extern "C" {
#endif

/*
 * redis config
 */
#define HOSTNAME "127.0.0.1"

#define REDIS_PORT 6379

/*
 * modbus config
 */

#define DEFAULT_MB_PORT "/dev/cu.usbserial-1130"
#define DEFAULT_MB_BAUD 115200
#define MB_PARITY 'N'
#define MB_DATA_BIT 8
#define MB_STOP_BIT 1
#define MB_TIMEOUT_S 0
#define MB_TIMEOUT_US 200000

#define MB_NAMESPACE "modbus"

#define MB_COIL_NAMESPACE MB_NAMESPACE ".coil"
#define MB_DI_NAMESPACE MB_NAMESPACE ".discrete_inputs"
#define MB_HR_NAMESPACE MB_NAMESPACE ".holding_registers"
#define MB_IR_NAMESPACE MB_NAMESPACE ".input_registers"

#define MB_READ_NAMESPACE ".read"
#define MB_WRITE_NAMESPACE ".write"

#define MB_REQUEST_NAMESPACE ".req"
#define MB_RESPONSE_NAMESPACE ".res"

#ifdef __cplusplus
}
#endif

#endif //MODBUS_CLIENT_CONFIG_H
