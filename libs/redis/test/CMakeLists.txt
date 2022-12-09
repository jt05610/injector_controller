file(
    GLOB_RECURSE
    REDIS_TEST_SOURCES
    *.*
)

include_directories(.)

add_executable(${REDIS_TESTS} ${REDIS_TEST_SOURCES})

target_link_libraries(${REDIS_TESTS} GTest::gtest_main ${REDIS_NODE_LIB})

gtest_discover_tests(${REDIS_TESTS})
