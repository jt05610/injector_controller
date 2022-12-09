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
