cmake_minimum_required(VERSION 3.10)
project(dining_philosophers C)

set(CMAKE_C_STANDARD 17)
set(CMAKE_CXX_FLAGS "-Wall -Wextra")

find_package(Curses REQUIRED)
find_package(Threads REQUIRED)

add_executable(dining_philosophers main.c)

target_link_libraries(dining_philosophers
    ${CMAKE_THREAD_LIBS_INIT}
    ${CURSES_LIBRARIES}
    m
)
