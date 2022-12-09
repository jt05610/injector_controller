file(
    GLOB_RECURSE
    MODBUS_TEST_SOURCES
    *.*
)

include_directories(.)

add_executable(${MODBUS_TESTS} ${MODBUS_TEST_SOURCES})

target_link_libraries(${MODBUS_TESTS} GTest::gtest_main ${MB_LIB})

gtest_discover_tests(${MODBUS_TESTS})
