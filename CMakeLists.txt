cmake_minimum_required(VERSION 3.21)

set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 17)

add_link_options(-Wno-dev)

add_definitions(
    -DCMAKE_C_FLAGS_DEBUG="-g -O0"
    -DCMAKE_CXX_FLAGS_DEBUG="-g -O0"
)

project(injector_controller C CXX)

set(MB_LIB modbus_client)
set(REDIS_NODE_LIB redis_node)
set(SERVICE_LAYER_LIB services)

set(REDIS_TESTS RedisTests)
set(MODBUS_TESTS ModbusTests)
set(RS485_INTERFACE_TESTS RS485InterfaceTests)

include(FetchContent)

include_directories(include)
if(${CMAKE_BUILD_TYPE} MATCHES "Debug")
    set(BUILD_TESTS 1)
    FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
    )

    # For Windows: Prevent overriding the parent project's compiler/linker settings
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

    FetchContent_MakeAvailable(googletest)

    enable_testing()
    include(GoogleTest)
else()
    set(BUILD_TESTS 0)
endif()

add_subdirectory(libs/modbus)
add_subdirectory(libs/redis)

add_subdirectory(nodes/rs485_interface)

