cmake_minimum_required(VERSION 3.12 FATAL_ERROR)

project(ssentencepiece)

set(SBPE_VERSION "0.2")

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")

set(CMAKE_SKIP_BUILD_RPATH FALSE)
set(BUILD_RPATH_USE_ORIGIN TRUE)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

if(NOT APPLE)
  set(SBPE_RPATH_ORIGIN "$ORIGIN")
else()
  set(SBPE_RPATH_ORIGIN "@loader_path")
endif()

set(CMAKE_INSTALL_RPATH ${SBPE_RPATH_ORIGIN})
set(CMAKE_BUILD_RPATH ${SBPE_RPATH_ORIGIN})

option(SBPE_ENABLE_TESTS "Whether to build tests" OFF)
option(SBPE_BUILD_PYTHON "Whether to build Python" ON)
option(BUILD_SHARED_LIBS "Whether to build shared libraries" ON)

if(NOT CMAKE_BUILD_TYPE)
  message(STATUS "No CMAKE_BUILD_TYPE given, default to Release")
  set(CMAKE_BUILD_TYPE Release)
endif()


list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake/Modules)
list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)

include(CheckCXXCompilerFlag)

# Directly set C++14 without checking
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

message(STATUS "C++ Standard version: ${CMAKE_CXX_STANDARD}")

if(SBPE_BUILD_PYTHON)
  include(pybind11)
endif()

include_directories(${CMAKE_SOURCE_DIR})

# 根据编译器类型设置不同的警告标志
if(MSVC)
  # MSVC 编译器的警告标志
  add_compile_options(/wd4244 /wd4267)
else()
  # GCC/Clang 编译器的警告标志
  add_compile_options(-Wno-unused-result -Wno-sign-compare)
endif()

if(SBPE_ENABLE_TESTS)
  include(googletest)
  enable_testing()
endif()

add_subdirectory(ssentencepiece)
