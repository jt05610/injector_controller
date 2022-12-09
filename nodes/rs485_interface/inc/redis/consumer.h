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

typedef struct redis_subscriber_t * RedisSubscriber;

typedef struct redis_subscription_t * RedisSubscription;

RedisSubscriber redis_subscriber_create();

typedef void (* subscribe_callback_t)(
        redisAsyncContext * c, void * reply, void * privdata);

RedisSubscription
redis_subscription_create(char * channel, subscribe_callback_t callback);

void redis_subscription_destroy(RedisSubscription subscription);

void redis_subscriber_destroy(RedisSubscriber base);

void
redis_subscribe(RedisSubscriber subscriber, RedisSubscription subscription);

void
redis_unsubscribe(RedisSubscriber subscriber, RedisSubscription subscription);

void redis_psubscribe(RedisSubscriber base, RedisSubscription subscription);

#ifdef __cplusplus
}
#endif

#endif //MODBUS_CLIENT_CONSUMER_H
