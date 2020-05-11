INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_HAM ham)

FIND_PATH(
    HAM_INCLUDE_DIRS
    NAMES ham/api.h
    HINTS $ENV{HAM_DIR}/include
        ${PC_HAM_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    HAM_LIBRARIES
    NAMES gnuradio-ham
    HINTS $ENV{HAM_DIR}/lib
        ${PC_HAM_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/hamTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(HAM DEFAULT_MSG HAM_LIBRARIES HAM_INCLUDE_DIRS)
MARK_AS_ADVANCED(HAM_LIBRARIES HAM_INCLUDE_DIRS)
