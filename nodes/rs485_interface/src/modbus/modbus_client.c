/**
  ******************************************************************************
  * @file   modbus_client.c
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

#include <stddef.h>
#include <modbus.h>
#include <stdlib.h>
#include <printf.h>
#include "modbus/modbus_client.h"
#include "config.h"


typedef enum modbus_client_state_t
{
    MB_IDLE,
    MB_CONNECTED,
} modbus_client_state_t;


typedef struct modbus_client_t
{
    modbus_client_state_t state;
    modbus_t    * client;
    char        * device;
    mb_result_t * result;
    int baud;
    void * data;
} modbus_client_t;


ModbusPDU
mb_pdu_create(
        uint8_t to, mb_func_code_t func_code, uint16_t addr, uint16_t nb,
        void * callback)
{
    static void * func_code_handlers[6] = {
            modbus_read_bits,
            modbus_read_input_bits,
            modbus_read_registers,
            modbus_read_input_registers,
            modbus_write_bit,
            modbus_write_register,
    };

    ModbusPDU result = calloc(1, sizeof(modbus_pdu_t));
    result->handler      = func_code_handlers[func_code - 1];
    result->mb_req       = calloc(1, sizeof(mb_req_t));
    result->mb_req->addr = addr;
    result->mb_req->nb   = nb;
    result->to           = to;
    result->privdata     = callback;
    result->func_code    = func_code;
    return result;
}

void
modbus_client_request(ModbusClient base, ModbusRequest request)
{
    if (base->state == MB_CONNECTED)
    {
        modbus_set_slave(base->client, request->pdu->to);
        if (request->pdu->func_code < MB_WRITE_COIL)
        {
            /*
             * Read functions
             */
            if (request->pdu->func_code < MB_READ_HR)
            {
                /*
                 * Bitwise access
                 */
                request->pdu->handler(
                        base->client, request->pdu->mb_req->addr,
                        request->pdu->mb_req->nb, base->result->small);
            } else
            {
                /*
                 * Register access
                 */
                request->pdu->handler(
                        base->client, request->pdu->mb_req->addr,
                        request->pdu->mb_req->nb, base->result->big);
            }

        } else
        {
            /*
            * write functions
            */
            int ok = request->pdu->handler(
                    base->client, request->pdu->mb_req->addr,
                    request->pdu->mb_req->nb);
            base->result->small[0] = (ok == 1) ? 1 : 0;
        }
        request->callback(base->result, request->pdu->privdata, base->data);
    }
}

ModbusClient
modbus_client_create(void * data)
{
    ModbusClient base = calloc(1, sizeof(modbus_client_t));

    base->baud   = DEFAULT_MB_BAUD;
    base->device = DEFAULT_MB_PORT;
    base->data   = data;
    base->client = modbus_new_rtu(
            base->device,
            base->baud,
            MB_PARITY,
            MB_DATA_BIT,
            MB_STOP_BIT
    );
    base->state  = MB_IDLE;
    modbus_set_response_timeout(base->client, MB_TIMEOUT_S, MB_TIMEOUT_US);
    base->result = calloc(RESULT_BUFFER_SIZE, sizeof(mb_result_t));
    return base;
}

void modbus_client_connect(ModbusClient base)
{
    if (modbus_connect(base->client) == -1)
    {
        modbus_free(base->client);
        base->state = MB_IDLE;
    } else
    {
        base->state = MB_CONNECTED;
        printf("connected!");

    }
}

void
modbus_client_set_device(ModbusClient base, char * device)
{
    base->device = device;
    if (base->state == MB_CONNECTED)
    {
        modbus_client_disconnect(base);
    }
    base->client = modbus_new_rtu(
            base->device,
            base->baud,
            MB_PARITY,
            MB_DATA_BIT,
            MB_STOP_BIT
    );
}

void
modbus_client_disconnect(ModbusClient base)
{
    modbus_close(base->client);
    base->state = MB_CONNECTED;
}

ModbusRequest
modbus_request_create(ModbusPDU pdu, modbus_callback_t callback)
{
    ModbusRequest result = calloc(1, sizeof(modbus_request_t));
    result->pdu      = pdu;
    result->callback = callback;
    return result;
}

void
modbus_requests_destroy(ModbusRequest request)
{
    free(request);
}

void
modbus_pdu_destroy(ModbusPDU pdu)
{
    free(pdu);
}

void
modbus_client_destroy(ModbusClient base)
{
    if (base->state == MB_CONNECTED)
    {
        modbus_client_disconnect(base);
        modbus_flush(base->client);
        modbus_free(base->client);
    }
    free(base->result);
    free(base);
}
