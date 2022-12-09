/**
  ******************************************************************************
  * @file   test_redis_publisher.cpp
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
#include "redis/publisher.h"

#if 0
class RedisPublisherTest : public ::testing::Test {
public:
    RedisPublisher publisher;
protected:
    void SetUp() override {
        publisher = redis_publisher_create(0);
    }
    void TearDown() override {
        redis_publisher_destroy(publisher);
    }
};


TEST_F(RedisPublisherTest, publish)
{
    redis_publish(publisher, "test", (char *)"test_msg");
}
#endif