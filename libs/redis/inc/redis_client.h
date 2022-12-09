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


#ifdef __cplusplus
extern "C" {
#endif

#include "subscriber.h"

typedef struct redis_client_t * RedisClient;

RedisClient redis_client_create(size_t n_subs);

void redis_client_attach(RedisClient base);

void redis_client_destroy(RedisClient base);

void
redis_client_publish(RedisClient base, const char * channel, char * message);

void redis_client_new_sub(RedisClient base, char * channel, r_cb_t callback);

void redis_client_subscribe(RedisClient base);

void redis_client_unsubscribe(RedisClient base);

void redis_client_run(RedisClient base);

void redis_client_spin_once(RedisClient base);

#ifdef __cplusplus
}
#endif

#endif //MODBUS_CLIENT_REDIS_CLIENT_H
