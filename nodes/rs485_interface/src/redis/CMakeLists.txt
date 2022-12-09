

include_directories(
)

file(
    GLOB_RECURSE
    REDIS_SOURCES
    *.*
)

add_library(${REDIS_NODE_LIB} ${REDIS_SOURCES})

target_link_libraries(${REDIS_NODE_LIB} hiredis ${LIBEVENT})


