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

#include "base.h"

EventBase stoppable_event_base(int fd, int on);

void stoppable_event_teardown(EventBase se);

void redis_publish_to_test(RedisBase base, char * msg, r_cb_t cb);

#endif //MODBUS_CLIENT_FIXTURES_H
