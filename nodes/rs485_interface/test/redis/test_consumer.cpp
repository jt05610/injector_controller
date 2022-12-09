/**
  ******************************************************************************
  * @file   test_redis_subscriber.cpp
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
#include <gtest/gtest.h>
#include "redis/consumer.h"


class RedisSubscriberTest : public ::testing::Test {
protected:
    void SetUp() override {
        subscriber = redis_subscriber_create();
    }
    void TearDown() override {
        redis_subscriber_destroy(subscriber);
    }
    RedisSubscriber subscriber;
};


TEST_F(RedisSubscriberTest, Fails)
{
    EXPECT_STRNE("hello", "world");
    EXPECT_EQ(1+1, 2);
}