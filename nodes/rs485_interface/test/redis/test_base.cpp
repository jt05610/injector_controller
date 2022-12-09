/**
  ******************************************************************************
  * @file   test_base.cpp
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
#include "redis/base.h"
#include "fixtures.h"

extern "C" {

#include <event2/event.h>
}

bool called;

class RedisBaseTest : public ::testing::Test
{
protected:
    void SetUp() override
    {
        base   = redis_base_create();
        eb     = stoppable_event_base(redis_base_get_fd(base));
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

void cb(redisAsyncContext * c, void * reply, void * privdata)
{
    (void) c;
    (void) reply;
    (void) privdata;
    called = true;
}

TEST_F(RedisBaseTest, execute_command)
{
    redis_publish_to_test(base, (char *) "1 0 1", cb);
    ASSERT_TRUE(event_base_dispatch(eb) == 0);
    ASSERT_TRUE(called);
}
