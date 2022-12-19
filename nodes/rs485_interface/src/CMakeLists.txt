set(
    RS485_INT_SOURCES
    adapters.c
    app.c
    handlers.c
)

add_library(${RS485_INT_LIB} ${RS485_INT_SOURCES})

target_link_libraries(${RS485_INT_LIB} ${MB_LIB} ${REDIS_NODE_LIB})

add_executable(${RS485_INT_RUNNER} main.c)

target_link_libraries(${RS485_INT_RUNNER} ${RS485_INT_LIB})

