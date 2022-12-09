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
#ifdef __cplusplus
extern "C" {
#endif
#include "config.h"
#define AND " "

#define MB_READ_COIL_REQ_CHANNEL MB_COIL_NAMESPACE MB_READ_NAMESPACE MB_REQUEST_NAMESPACE
#define MB_READ_COIL_RES_CHANNEL MB_COIL_NAMESPACE MB_READ_NAMESPACE MB_RESPONSE_NAMESPACE

#define MB_READ_DI_REQ_CHANNEL MB_DI_NAMESPACE MB_READ_NAMESPACE MB_REQUEST_NAMESPACE
#define MB_READ_DI_RES_CHANNEL MB_DI_NAMESPACE MB_READ_NAMESPACE MB_RESPONSE_NAMESPACE

#define MB_READ_HR_REQ_CHANNEL MB_HR_NAMESPACE MB_READ_NAMESPACE MB_REQUEST_NAMESPACE
#define MB_READ_HR_RES_CHANNEL MB_HR_NAMESPACE MB_READ_NAMESPACE MB_RESPONSE_NAMESPACE

#define MB_READ_IR_REQ_CHANNEL MB_IR_NAMESPACE MB_READ_NAMESPACE MB_REQUEST_NAMESPACE
#define MB_READ_IR_RES_CHANNEL MB_IR_NAMESPACE MB_READ_NAMESPACE MB_RESPONSE_NAMESPACE

#define MB_WRITE_COIL_REQ_CHANNEL MB_COIL_NAMESPACE MB_WRITE_NAMESPACE MB_REQUEST_NAMESPACE
#define MB_WRITE_COIL_RES_CHANNEL MB_COIL_NAMESPACE MB_WRITE_NAMESPACE MB_RESPONSE_NAMESPACE

#define MB_WRITE_HR_REQ_CHANNEL MB_HR_NAMESPACE MB_WRITE_NAMESPACE MB_REQUEST_NAMESPACE
#define MB_WRITE_HR_RES_CHANNEL MB_HR_NAMESPACE MB_WRITE_NAMESPACE MB_RESPONSE_NAMESPACE

#define MB_SUBSCRIPTIONS    MB_READ_COIL_REQ_CHANNEL AND \
                            MB_READ_DI_REQ_CHANNEL AND \
                            MB_READ_HR_REQ_CHANNEL AND \
                            MB_READ_IR_REQ_CHANNEL AND \
                            MB_WRITE_COIL_REQ_CHANNEL AND \
                            MB_WRITE_HR_REQ_CHANNEL

typedef struct app_t * App;

App app_create();

void app_destroy(App app);

void app_run(App app);

#ifdef __cplusplus
}
#endif

#endif //MODBUS_CLIENT_APP_H
