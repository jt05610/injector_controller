/**
  ******************************************************************************
  * @file   test_mb_client.cpp
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
#include "../inc/modbus_client.h"

static uint8_t i;

class ModbusClientTest : public ::testing::Test
{
protected:
    void SetUp() override
    {
        client = modbus_client_create(0);
         i = 0;
    }

    void TearDown() override
    {
        modbus_client_destroy(client);
        modbus_pdu_destroy(result);
        modbus_requests_destroy(request);
    }

    ModbusClient  client;
    ModbusPDU     result;
    ModbusRequest request;
};


void mb_callback(mb_result_t * result, void * data, void * privdata)
{
    i = 0xFF;
}

TEST_F(ModbusClientTest, request)
{
    result = mb_pdu_create(0x01, MB_READ_COILS, 0x00, 0x01, 0);
    request = modbus_request_create(result, mb_callback);
    modbus_client_connect(client);
    modbus_client_request(client, request);
    ASSERT_EQ(0xFF, i);
}
