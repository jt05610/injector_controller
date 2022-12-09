
add_library(${MB_CLIENT_LIB} ${MODBUS_SOURCES})

target_link_libraries(${MB_CLIENT_LIB} ${MODBUS_LIB})
