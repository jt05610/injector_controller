/**
  ******************************************************************************
  * @file   test_base.cpp
  * @author Jonathan Taylor
  * @date   12/7/22
  * @brief  GTests for testing redis base.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2022 Jonathan Taylor.
  * All rights reserved.
  *
  ******************************************************************************
  */

#include <gtest/gtest.h>
#include "base.h"
#include "fixtures.h"
#include <event2/event.h>

bool called;

class RedisBaseTest : public ::testing::Test
{
protected:
    void SetUp() override
    {
        base   = redis_base_create();
        eb     = stoppable_event_base(redis_base_get_fd(base), EV_READ);
        called = false;
        ASSERT_TRUE(eb != nullptr);
        redis_base_attach(base, eb);
    }

    void TearDown() override
    {
        stoppable_event_teardown(eb);
    }

    RedisBase base;
    struct event_base * eb;
};

void output_cb(redisAsyncContext * c, void * reply, void * privdata)
{
    (void) c;
    (void) reply;
    (void) privdata;
    called = true;
}

TEST_F(RedisBaseTest, execute_command)
{
    redis_publish_to_test(base, (char *) "1 0 1", output_cb);
    ASSERT_TRUE(event_base_dispatch(eb) == 0);
    ASSERT_TRUE(called);
}
