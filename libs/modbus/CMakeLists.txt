if(UNIX AND NOT APPLE)
    # linux
    set(LIB_SEARCH_DIR "/opt/homebrew/lib")
    set(MODBUS_INC_DIR /opt/homebrew/include/modbus)
elseif(UNIX)
    # mac
    set(LIB_SEARCH_DIR "/opt/homebrew/lib")
    set(MODBUS_INC_DIR /opt/homebrew/include/modbus)
elseif(WIN32)
    # windows
    set(LIB_SEARCH_DIR "/opt/homebrew/lib")
    set(MODBUS_INC_DIR /opt/homebrew/include/modbus)
endif()

find_library(MODBUS_LIB NAMES libmodbus.dylib PATHS ${LIB_SEARCH_DIR})
message("${MODBUS_LIB-NOTFOUND}")

include_directories(
    inc
    ${MODBUS_INC_DIR}
)

add_subdirectory(src)
if(${BUILD_TESTS})
    add_subdirectory(test)
endif()



