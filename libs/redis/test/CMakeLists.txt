add_executable(${REDIS_TESTS})

file(
    GLOB_RECURSE
    REDIS_TEST_SOURCES
    *.*
)

target_sources(${REDIS_TESTS} PRIVATE ${REDIS_TEST_SOURCES})
target_include_directories(${REDIS_TESTS} PRIVATE .)
target_link_libraries(${REDIS_TESTS} PRIVATE GTest::gtest_main ${REDIS_NODE_LIB})

gtest_discover_tests(${REDIS_TESTS})
