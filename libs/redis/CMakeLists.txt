if(UNIX AND NOT APPLE)
    # linux
    set(LIBEVENT_PATH "/opt/homebrew/lib")
    set(LIBEVENT_NAME "libevent.dylib")
    set(LIBEVENT_INC /opt/homebrew/Cellar/libevent/2.1.12/include)
elseif(UNIX)
    # mac
    set(LIBEVENT_PATH "/opt/homebrew/lib")
    set(LIBEVENT_NAME "libevent.dylib")
    set(LIBEVENT_INC /opt/homebrew/Cellar/libevent/2.1.12/include)
elseif(WIN32)
    # windows
    set(LIBEVENT_PATH "/opt/homebrew/lib")
    set(LIBEVENT_NAME "libevent.dylib")
    set(LIBEVENT_INC /opt/homebrew/Cellar/libevent/2.1.12/include)
endif()

FetchContent_Declare(
    hiredis
    GIT_REPOSITORY https://github.com/redis/hiredis.git
    GIT_TAG v1.1.0
)

FetchContent_MakeAvailable(hiredis)

find_library(LIBEVENT_LIB NAMES ${LIBEVENT_NAME} PATHS ${LIBEVENT_PATH})
message("${LIBEVENT_LIB-NOTFOUND}")

include_directories(
    inc
    ${LIBEVENT_INC}
    ${hiredis_SOURCE_DIR}
)

add_subdirectory(src)
if(${BUILD_TESTS})
    add_subdirectory(test)
endif()