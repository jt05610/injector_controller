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
        i      = 0;
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
    uint32_t msgs  = 1;
    uint32_t total = msgs;
    bool     val   = false;
    result  = mb_pdu_create(0x01, MB_READ_IR, 0x00, 1, 0);
    request = modbus_request_create(result, mb_callback);
    modbus_client_connect(client);
    uint8_t  retries      = 5;
    uint16_t total_errors = 0;
    while (msgs--) {
        i   = 0;
        val = !val;
        result->mb_req->nb = val;
        request = modbus_request_create(result, mb_callback);
        while (modbus_client_request(client, request) != 1) {
            total_errors++;
            retries--;
            if (retries == 0) {
                printf(
                        "\nTotal messages:      %u"
                        "\nTotal errors:        %u"
                        "\n",
                        total,
                        total_errors
                );
                FAIL();
            }
        }
        retries = 5;
    }
    printf(
            "\nTotal messages:      %u"
            "\nTotal errors:        %u"
            "\n",
            total,
            total_errors
    );
}
