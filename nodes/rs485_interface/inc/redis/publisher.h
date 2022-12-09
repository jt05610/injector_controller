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

#include <adapters/macosx.h>

typedef struct redis_publisher_t * RedisPublisher;

RedisPublisher redis_publisher_create(CFRunLoopRef loop);

void redis_publisher_destroy(RedisPublisher base);

void redis_publish(RedisPublisher base, const char * channel, char * message);

#ifdef __cplusplus
}
#endif

#endif //MODBUS_CLIENT_PUBLISHER_H
