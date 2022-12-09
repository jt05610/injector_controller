file(
    GLOB_RECURSE
    SERVICE_LAYER_SOURCES
    *.*
)

#fetchcontent_declare(
#    CJSON
#    GIT_REPOSITORY https://github.com/DaveGamble/cJSON.git
#    GIT_TAG v1.7.15
#)
# fetchcontent_makeavailable(CJSON)


add_library(${SERVICE_LAYER_LIB} ${SERVICE_LAYER_SOURCES})

target_link_libraries(${SERVICE_LAYER_LIB} ${MB_CLIENT_LIB} ${REDIS_NODE_LIB})
