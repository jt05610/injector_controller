/**
  ******************************************************************************
  * @file   redis_publisher.h
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

#ifndef MODBUS_CLIENT_PUBLISHER_H
#define MODBUS_CLIENT_PUBLISHER_H

#ifdef __cplusplus
extern "C" {
#endif

#include "base.h"

typedef struct redis_pub_t * RedisPub;

RedisPub redis_pub_create();

void redis_pub_attach(RedisPub base, EventBase eb);

void redis_pub_destroy(RedisPub base);

void redis_publish(RedisPub base, const char * channel, char * message);

void redis_pub_set_data(RedisPub base, void * data);

#ifdef __cplusplus
}
#endif

#endif //MODBUS_CLIENT_PUBLISHER_H
