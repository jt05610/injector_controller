/**
  ******************************************************************************
  * @file   test_handlers.cpp
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

#include <gtest/gtest.h>
#include "adapters.h"

TEST(adapters, redis_to_modbus)
{
    char str[] = "23 1234 12345";
    ModbusRequest result;
    result = redis_to_modbus(str, MB_READ_COILS, 0, 0);
    ModbusPDU pdu = result->pdu;
    ASSERT_EQ(MB_READ_COILS, pdu->func_code);
    ASSERT_EQ(23, pdu->to);
    ASSERT_EQ(1234, pdu->mb_req->addr);
    ASSERT_EQ(12345, pdu->mb_req->nb);
}
