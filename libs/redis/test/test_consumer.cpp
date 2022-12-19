/**
  ******************************************************************************
  * @file   test_consumer.cpp
  * @author Jonathan Taylor
  * @date   12/6/22
  * @brief  GTests for redis consumer
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2022 Jonathan Taylor.
  * All rights reserved.
  *
  ******************************************************************************
  */
#include <gtest/gtest.h>
#include <event2/event.h>
#include "subscriber.h"
#include "fixtures.h"

static bool called;

static void output_cb(redisAsyncContext * c, void * reply, void * privdata);

class RedisSubscriberTest : public ::testing::Test
{
protected:
    void SetUp() override
    {
        called     = false;
        subscriber = redis_sub_create(2);
        publisher  = redis_base_create();
        eb_sub     = event_base_new();
        redis_sub_attach(subscriber, eb_sub);
        redis_base_attach(publisher, eb_sub);
        redis_sub_add(subscriber, (char *) "test", output_cb);
    }

    void TearDown() override
    {
        redis_sub_destroy(subscriber);
        event_base_free(eb_sub);
    }

    EventBase eb_sub;
    RedisSub  subscriber;
    RedisBase publisher;

    void run_loops()
    {
        while (!called)
        {
            event_base_loop(eb_sub, EVLOOP_NONBLOCK);
        }
    }
};

TEST_F(RedisSubscriberTest, subscribe)
{
    redis_subscribe(subscriber);
    redis_publish_to_test(publisher, (char *) "1 0 1", 0);
    run_loops();
    ASSERT_TRUE(called);
}

static void
output_cb(redisAsyncContext * c, void * reply, void * privdata)
{
    (void) c;
    (void) privdata;
    redisReply * rpl = (redisReply *) reply;
    if (rpl == NULL)
    {
        return;
    }
    char * msg = rpl->element[2]->str;
    if (msg != NULL)
    {
        called = true;
    }
}