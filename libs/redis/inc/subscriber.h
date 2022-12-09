/**
  ******************************************************************************
  * @file   redis_subscriber.h
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

#ifndef MODBUS_CLIENT_CONSUMER_H
#define MODBUS_CLIENT_CONSUMER_H

#include "base.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct redis_sub_t * RedisSub;

RedisSub redis_sub_create(size_t max_subs);

void redis_sub_add(RedisSub base, char * channel, r_cb_t callback);

void redis_sub_attach(RedisSub subscriber, struct event_base * eb);

void redis_sub_destroy(RedisSub base);

void redis_subscribe(RedisSub subscriber);

void redis_unsubscribe(RedisSub subscriber);

#ifdef __cplusplus
}
#endif

#endif //MODBUS_CLIENT_CONSUMER_H
