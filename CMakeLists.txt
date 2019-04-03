cmake_minimum_required(VERSION 2.8.12)
project(smpeg2)

include(conanbuildinfo.cmake)
conan_basic_setup()

option(CONTROLS OFF "Embeed media player controls")

if(NOT CONTROLS)
    add_definitions(-DNOCONTROLS)
endif()

file(GLOB SOURCES
  ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/MPEG*.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/smpeg.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/audio/*.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/video/*.cpp)

file(GLOB HEADERS
  ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/MPEG*.h
  ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/smpeg.h
  ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/audio/*.h
  ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/video/*.h)

file(GLOB PUBLIC_HEADERS
  ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/MPEG*.h
  ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/smpeg.h)
  
  message(STATUS "PUBLIC_HEADERS ${PUBLIC_HEADERS}")
  
add_library(${PROJECT_NAME} ${SOURCES} ${HEADERS})

target_link_libraries(${PROJECT_NAME} PRIVATE ${CONAN_LIBS})

target_include_directories(${PROJECT_NAME} PRIVATE "source_subfolder")

if(CMAKE_COMPILER_IS_GNUCC AND NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 6.0)
	target_compile_options(${PROJECT_NAME} PRIVATE -Wno-narrowing)
endif()

if(CMAKE_CXX_COMPILER_ID MATCHES "Clang" AND NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 6.0)
    target_compile_options(${PROJECT_NAME} PRIVATE -Wno-c++11-narrowing)
endif()

install(TARGETS ${PROJECT_NAME}
  ARCHIVE DESTINATION "lib"
  LIBRARY DESTINATION "lib"
  RUNTIME DESTINATION "bin"
)

install(FILES ${PUBLIC_HEADERS} DESTINATION "include/smpeg2" COMPONENT devel)
