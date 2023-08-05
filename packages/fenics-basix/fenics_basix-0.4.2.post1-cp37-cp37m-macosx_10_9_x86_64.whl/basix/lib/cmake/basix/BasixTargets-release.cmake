#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Basix::basix" for configuration "Release"
set_property(TARGET Basix::basix APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Basix::basix PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libbasix.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libbasix.dylib"
  )

list(APPEND _IMPORT_CHECK_TARGETS Basix::basix )
list(APPEND _IMPORT_CHECK_FILES_FOR_Basix::basix "${_IMPORT_PREFIX}/lib/libbasix.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
