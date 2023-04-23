cmake_minimum_required(VERSION 3.15)
cmake_policy(SET CMP0074 NEW)

project(test_package LANGUAGES CXX)
set(CMAKE_VERBOSE_MAKEFILE TRUE)

find_package(aruco REQUIRED CONFIG)
find_package(OpenCV REQUIRED MODULE)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE aruco::aruco opencv::opencv)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_11)