set(RS485_INT_LIB rs485_interface)
set(RS485_INT_RUNNER RunRS485Interface)

include_directories(
    inc
    ../../libs/modbus/inc
    ../../libs/redis/inc
)

add_subdirectory(src)

if(${BUILD_TESTS})
    add_subdirectory(test)
endif()