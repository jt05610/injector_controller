file(
    GLOB_RECURSE
    RS485_INTERFACE_TEST_SOURCES
    *.*
)
include_directories(.)

add_executable(${RS485_INTERFACE_TESTS} ${RS485_INTERFACE_TEST_SOURCES})

target_link_libraries(${RS485_INTERFACE_TESTS} GTest::gtest_main ${RS485_INT_LIB})

gtest_discover_tests(${RS485_INTERFACE_TESTS})
