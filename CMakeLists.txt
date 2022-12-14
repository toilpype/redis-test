CMAKE_MINIMUM_REQUIRED(VERSION 2.4)
PROJECT(sender)

option(LINK_SHARED_ZED "Link with the ZED SDK shared executable" ON)

if (NOT LINK_SHARED_ZED AND MSVC)
    message(FATAL_ERROR "LINK_SHARED_ZED OFF : ZED SDK static libraries not available on Windows")
endif()

if(COMMAND cmake_policy)
	cmake_policy(SET CMP0003 OLD)
	cmake_policy(SET CMP0015 OLD)
endif(COMMAND cmake_policy)

SET(EXECUTABLE_OUTPUT_PATH ".")

IF(NOT MSVC)
    SET(SPECIAL_OS_LIBS "pthread" "X11")
ENDIF()

find_package(ZED 3 REQUIRED)
find_package(OpenCV REQUIRED)
find_package(CUDA ${ZED_CUDA_VERSION} REQUIRED)
find_path(HIREDIS_HEADER hiredis)
find_path(REDIS_PLUS_PLUS_HEADER sw)
# find_package(msgpack REQUIRED)

include_directories(${CUDA_INCLUDE_DIRS})
include_directories(${ZED_INCLUDE_DIRS})
include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(${HIREDIS_HEADER})
include_directories(${REDIS_PLUS_PLUS_HEADER})

find_library(HIREDIS_LIB hiredis)
find_library(REDIS_PLUS_PLUS_LIB redis++)

link_directories(${ZED_LIBRARY_DIR})
link_directories(${OpenCV_LIBRARY_DIRS})
link_directories(${CUDA_LIBRARY_DIRS})
link_directories(${HIREDIS_LIB})
link_directories(${REDIS_PLUS_PLUS_LIB})

ADD_EXECUTABLE(${PROJECT_NAME} src/sender.cpp)

add_definitions(-std=c++14 -O3)

if (LINK_SHARED_ZED)
    SET(ZED_LIBS ${ZED_LIBRARIES} ${CUDA_CUDA_LIBRARY} ${CUDA_CUDART_LIBRARY} ${SPECIAL_OS_LIBS})
else()
    SET(ZED_LIBS ${ZED_STATIC_LIBRARIES} ${CUDA_CUDA_LIBRARY} ${CUDA_LIBRARY} ${SPECIAL_OS_LIBS})
endif()

TARGET_LINK_LIBRARIES(${PROJECT_NAME} ${ZED_LIBS} ${SPECIAL_OS_LIBS} ${OpenCV_LIBRARIES} ${HIREDIS_LIB} ${REDIS_PLUS_PLUS_LIB})
# target_link_libraries(${PROJECT_NAME} msgpackc-cxx)
