file(
    GLOB_RECURSE
    MODBUS_SOURCES
    *.*
)

add_library(${MB_LIB} ${MODBUS_SOURCES})

target_link_libraries(${MB_LIB} ${MODBUS_LIB})
