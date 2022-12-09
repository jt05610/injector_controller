/**
  ******************************************************************************
  * @file   test_publisher.cpp
  * @author Jonathan Taylor
  * @date   12/6/22
  * @brief  GTests for testing redis publisher.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2022 Jonathan Taylor.
  * All rights reserved.
  *
  ******************************************************************************
  */

#include <gtest/gtest.h>
#include "publisher.h"
#include "subscriber.h"

static char * expected;
static bool passed;

static void pub_test_cb(redisAsyncContext * c, void * reply, void * privdata);

class RedisPublisherTest : public ::testing::Test
{
protected:
    void SetUp() override
    {
        subscriber = redis_sub_create(1);
        publisher  = redis_pub_create();
        eb         = event_base_new();
        passed     = false;
        redis_sub_add(subscriber, (char *) "pub_test", pub_test_cb);
        redis_sub_attach(subscriber, eb);
        redis_pub_attach(publisher, eb);
        redis_subscribe(subscriber);
    }

    void TearDown() override
    {
        redis_pub_destroy(publisher);
        redis_sub_destroy(subscriber);
    }

    void expect(char * value)
    {
        expected = (char *) calloc(strlen(value) + 1, sizeof(char));
        strcpy(expected, value);
    }

    void run_loops(uint8_t max_iter)
    {
        while (max_iter)
        {
            if (passed)
            {
                break;
            }
            event_base_loop(eb, EVLOOP_NONBLOCK);
            max_iter--;
        }
    }

    EventBase eb;
    RedisPub  publisher;
    RedisSub  subscriber;
};

TEST_F(RedisPublisherTest, publish)
{
    const char * msg = "test_msg";
    expect((char *) msg);
    redis_publish(publisher, "pub_test", (char *) msg);
    run_loops(100);
    ASSERT_TRUE(passed);
}

static void
pub_test_cb(redisAsyncContext * c, void * reply, void * privdata)
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
        if (strcmp(expected, msg) == 0)
        {
            passed = true;
        }
    }
}