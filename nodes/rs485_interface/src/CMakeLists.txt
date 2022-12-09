
file(GLOB_RECURSE SOURCES */*.* *.*)
add_executable(runner main.c)

target_link_libraries(runner ${LIBS})

file(
    GLOB_RECURSE
    SERVICE_LAYER_SOURCES
    *.*
)

add_library(${SERVICE_LAYER_LIB} ${SERVICE_LAYER_SOURCES})

target_link_libraries(${SERVICE_LAYER_LIB} ${MB_CLIENT_LIB} ${REDIS_NODE_LIB})
