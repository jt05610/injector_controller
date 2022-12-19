/**
  ******************************************************************************
  * @file   mb_config.h
  * @author Jonathan Taylor
  * @date   12/9/22
  * @brief  Default config for modbus client
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2022 Jonathan Taylor.
  * All rights reserved.
  *
  ******************************************************************************
  */

#ifndef INJECTOR_CONTROLLER_MB_CONFIG_H
#define INJECTOR_CONTROLLER_MB_CONFIG_H

#ifdef __cplusplus
extern "C" {
#endif

#define DEFAULT_MB_PORT "/dev/cu.usbserial-1140"
#define DEFAULT_MB_BAUD 115200
#define MB_PARITY 'N'
#define MB_DATA_BIT 8
#define MB_STOP_BIT 2
#define MB_TIMEOUT_S 0
#define MB_TIMEOUT_US 200000

#ifdef __cplusplus
}
#endif

#endif //INJECTOR_CONTROLLER_MB_CONFIG_H
