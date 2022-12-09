add_link_options(-Wno-dev)



file(
    GLOB_RECURSE
    MODBUS_SOURCES
    *.*
)

add_subdirectory(redis)
add_subdirectory(modbus)
add_subdirectory(service_layer)


add_definitions(
    -DCMAKE_C_FLAGS_DEBUG="-g -O0"
    -DCMAKE_CXX_FLAGS_DEBUG="-g -O0"
)

file(GLOB_RECURSE SOURCES */*.* *.*)
add_executable(runner main.c)

target_link_libraries(runner ${LIBS})