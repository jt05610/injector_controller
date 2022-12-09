/**
  ******************************************************************************
  * @file   modbus_test.cpp
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

#if 0
#include <stdio.h>
#define ID 0x01
#define RUN_TIME 5000

#include "modbus.h"

#include <time.h>
#include <stdbool.h>

#include "config.h"
void
modbus_test()
{
    modbus_t *client;

    client = modbus_new_rtu(PORT,BAUD, 'N', 8, 1);
    modbus_set_response_timeout(client, 1, 0);
    //modbus_set_debug(client, TRUE);
    modbus_set_slave(client, 0x01);
    modbus_connect(client);
    clock_t start;
    uint8_t dest[1];
    uint32_t msgs = 1000;
    clock_t diff;
    start = clock();
    while (msgs--)
    {
        modbus_read_input_bits(client, 0x00, 0x01, dest);
    }
    diff = clock() - start;
    int msec = diff * 1000 / CLOCKS_PER_SEC;
    long long messages_per_second = (1000 * 1000) / msec;
    printf("Total time: %i\n", msec);
    printf("Messages / s: %lli\n", messages_per_second);
    modbus_close(client);
    modbus_flush(client);
    modbus_free(client);
}
#endif