/**
  ******************************************************************************
  * @file   test_client.cpp
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

#include "redis_client.h"

#include "fixtures.h"
#include "publisher.h"

#define N_CHECKS 2

static char * expects[N_CHECKS];
static bool  passes[N_CHECKS];

static RedisClient _client;

static void sub_a_cb(redisAsyncContext * c, void * reply, void * privdata);
static void sub_b_cb(redisAsyncContext * c, void * reply, void * privdata);

static void sub_a_req_cb(redisAsyncContext * c, void * reply, void * privdata);
static void sub_b_req_cb(redisAsyncContext * c, void * reply, void * privdata);

class RedisClientTest : public ::testing::Test
{
protected:
    void SetUp() override
    {
        client = redis_client_create(2);
        _client = client;
        fake_sub = redis_sub_create(2);
        fake_pub = redis_pub_create();
        for (uint8_t i = 0; i < N_CHECKS; i ++) {
            passes[i] = false;
        }
        eb_watch = event_base_new();
        redis_sub_add(fake_sub, (char *) "chan_a.res", sub_a_cb);
        redis_sub_add(fake_sub, (char *) "chan_b.res", sub_b_cb);
        redis_client_new_sub(client, (char *) "chan_a.req", sub_a_req_cb);
        redis_client_new_sub(client, (char *) "chan_b.req", sub_b_req_cb);
        redis_sub_attach(fake_sub, eb_watch);
        redis_pub_attach(fake_pub, eb_watch);
        redis_client_attach(client);
        redis_subscribe(fake_sub);
        redis_client_subscribe(client);
    }

    void TearDown() override
    {
        redis_pub_destroy(fake_pub);
        redis_sub_destroy(fake_sub);
        event_base_free(eb_watch);
        for(uint8_t i = 0; i < N_CHECKS; i ++) {
            ASSERT_TRUE(passes[i]);
            free(expects[i]);
        }
    }

    EventBase   eb_watch;
    RedisSub    fake_sub;
    RedisPub    fake_pub;
    RedisClient client;

    void expect(uint8_t which, char * value)
    {
        expects[which] = (char *) calloc(strlen(value) + 1, sizeof(char));
        strcpy(expects[which], value);
    }

    void run_loops(uint16_t n_iter)
    {
        while (n_iter) {
            if (passes[0] && passes[1])
                break;
            event_base_loop(eb_watch, EVLOOP_NONBLOCK);
            redis_client_spin_once(client);
            n_iter--;
        }
    }
};

TEST_F(RedisClientTest, e2e)
{
    const char * chan_a = "chan_a.req";
    const char * chan_b = "chan_b.req";
    const char * msg_a = "hello";
    const char * msg_b = "world";
    redis_publish(fake_pub, (char *) chan_a, (char*)msg_a);
    redis_publish(fake_pub, (char *) chan_b, (char*)msg_b);
    expect(0, (char *)msg_a);
    expect(1, (char *)msg_b);
    run_loops(100);
}


static inline char *
extract(void * reply) {
    char * res = NULL;
    redisReply * rpl = (redisReply *)reply;
    if (rpl != NULL)
        res = rpl->element[2]->str;
    return res;
}

static inline void
_cb(uint8_t which, void * reply)
{
    char *msg = extract(reply);
    if(msg != NULL) {
        if(strcmp(expects[which], msg) == 0)
            passes[which] = true;
    }
}

static void
sub_a_cb(redisAsyncContext * c, void * reply, void * privdata)
{
    (void) c;
    (void) privdata;
    _cb(0, reply);
}

static void
sub_b_cb(redisAsyncContext * c, void * reply, void * privdata)
{
    (void) c;
    (void) privdata;
    _cb(1, reply);
}

static inline void
echo(const char * channel, char * message)
{
    redis_client_publish(_client, channel, message);
}

void
sub_a_req_cb(redisAsyncContext * c, void * reply, void * privdata)
{
    (void) c;
    (void) privdata;
    char * msg = extract(reply);
    if(msg != NULL) {
        echo("chan_a.res", msg);
    }
}

void
sub_b_req_cb(redisAsyncContext * c, void * reply, void * privdata)
{
    (void) c;
    (void) privdata;
    char * msg = extract(reply);
    if(msg != NULL) {
        echo("chan_b.res", msg);
    }
}
