/**
  ******************************************************************************
  * @file   fixtures.h
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

#ifndef MODBUS_CLIENT_FIXTURES_H
#define MODBUS_CLIENT_FIXTURES_H

#include "redis/base.h"

struct event_base * stoppable_event_base(int fd);

void stoppable_event_teardown(struct event_base * se);

void redis_publish_to_test(RedisBase base, char * msg, redis_callback_t cb);

#endif //MODBUS_CLIENT_FIXTURES_H
