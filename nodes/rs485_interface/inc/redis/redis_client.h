/**
  ******************************************************************************
  * @file   redis_pubsub.h
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

#ifndef MODBUS_CLIENT_REDIS_CLIENT_H
#define MODBUS_CLIENT_REDIS_CLIENT_H

#include "consumer.h"

typedef struct redis_client_t * RedisClient;

RedisClient redis_client_create();

void redis_client_destroy(RedisClient base);

void redis_client_publish(RedisClient base, const char * channel, char * message);

void redis_client_subscribe(RedisClient base, RedisSubscription subscription);

void redis_client_unsubscribe(RedisClient base, const char * channel);

void redis_client_psubscribe(RedisClient base, RedisSubscription subscription);

void redis_client_punsubscribe(RedisClient base, const char * channel);

void redis_stream(RedisClient base, const char * channel, char * data);

#endif //MODBUS_CLIENT_REDIS_CLIENT_H
