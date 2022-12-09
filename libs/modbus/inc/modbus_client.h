/**
  ******************************************************************************
  * @file   modbus_client.h
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

#ifndef MODBUS_CLIENT_MODBUS_CLIENT_H
#define MODBUS_CLIENT_MODBUS_CLIENT_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>

#define RESULT_BUFFER_SIZE 2

typedef struct modbus_pdu_t * ModbusPDU;

typedef struct modbus_client_t * ModbusClient;

typedef struct modbus_request_t * ModbusRequest;

typedef enum mb_func_code_t
{
    MB_READ_COILS     = 0x01,
    MB_READ_DI        = 0x02,
    MB_READ_HR        = 0x03,
    MB_READ_IR        = 0x04,
    MB_WRITE_COIL     = 0x05,
    MB_WRITE_REGISTER = 0x06,

} mb_func_code_t;

typedef union mb_result_t
{
    uint8_t  small[RESULT_BUFFER_SIZE];
    uint16_t big[RESULT_BUFFER_SIZE];

} mb_result_t;

typedef void(* modbus_callback_t)(mb_result_t * result, void * data, void * privdata);

typedef struct mb_req_t
{
    uint16_t addr;
    uint16_t nb;
}           mb_req_t;

typedef struct modbus_pdu_t
{
    uint8_t to;

    int (* handler)();

    void     * privdata;
    mb_req_t * mb_req;
    mb_func_code_t func_code;
}           modbus_pdu_t;

typedef struct modbus_request_t
{
    ModbusPDU         pdu;
    modbus_callback_t callback;
}           modbus_request_t;


ModbusClient modbus_client_create(void * data);

ModbusPDU mb_pdu_create(
        uint8_t to, mb_func_code_t func_code, uint16_t addr, uint16_t nb,
        void * callback);

ModbusRequest modbus_request_create(ModbusPDU pdu, modbus_callback_t callback);

void modbus_requests_destroy(ModbusRequest request);

void modbus_pdu_destroy(ModbusPDU pdu);

void modbus_client_destroy(ModbusClient base);

void modbus_client_connect(ModbusClient base);

void modbus_client_disconnect(ModbusClient base);

void modbus_client_set_device(ModbusClient base, char * device);

void modbus_client_request(ModbusClient base, ModbusRequest request);

#ifdef __cplusplus
}
#endif

#endif //MODBUS_CLIENT_MODBUS_CLIENT_H
