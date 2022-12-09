/**
  ******************************************************************************
  * @file   redis_pubsub.c
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

#include "redis/redis_client.h"
#include "redis/publisher.h"
#include "redis/consumer.h"

typedef struct redis_client_t {
    RedisPublisher publisher;
    RedisSubscriber subscriber;
} redis_client_t;

RedisClient redis_client_create(CFRunLoopRef loop)
{
    RedisClient base = calloc(1, sizeof(redis_client_t));
    base->publisher = redis_publisher_create(loop);
    base->subscriber = redis_subscriber_create(loop);
    return base;
}

void
redis_client_destroy(RedisClient base)
{
    redis_publisher_destroy(base->publisher);
    redis_subscriber_destroy(base->subscriber);
}

void redis_client_publish(RedisClient base, const char * channel, char * message)
{
    redis_publish(base->publisher, channel, message);
}

void redis_client_subscribe(RedisClient base, RedisSubscription subscription)
{
    redis_subscribe(base->subscriber, subscription);

}

void redis_client_psubscribe(RedisClient base, RedisSubscription subscription)
{
    redis_psubscribe(base->subscriber, subscription);
}
