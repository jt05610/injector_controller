cmake_minimum_required(VERSION 3.21)
project(modbus_client C CXX)

set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 17)

set(MB_CLIENT_LIB modbus_client)
set(REDIS_NODE_LIB redis_node)
set(SERVICE_LAYER_LIB services)

include(FetchContent)

FetchContent_Declare(
    hiredis
    GIT_REPOSITORY https://github.com/redis/hiredis.git
    GIT_TAG v1.1.0
)

FetchContent_MakeAvailable(hiredis)

set(BREW_LIB_PATH "/opt/homebrew/lib")
set(LIBEVENT_INC_DIR /opt/homebrew/Cellar/libevent/2.1.12/include)

find_library(MODBUS_LIB NAMES libmodbus.dylib PATHS ${BREW_LIB_PATH})

message("${MODBUS_LIB-NOTFOUND}")

find_library(LIBEVENT NAMES libevent.dylib PATHS ${BREW_LIB_PATH})

include_directories(
    /opt/homebrew/include/modbus
    ${hiredis_SOURCE_DIR}
    ${LIBEVENT_INC_DIR}
)
set(
    LIBS
    hiredis
    ${MB_CLIENT_LIB}
    ${REDIS_NODE_LIB}
    ${SERVICE_LAYER_LIB}
    ${LIBEVENT}
)

include_directories(inc)
add_subdirectory(src)
add_subdirectory(test)
