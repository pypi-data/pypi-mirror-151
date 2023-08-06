#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "scorer_edge::l2dc" for configuration "Release"
set_property(TARGET scorer_edge::l2dc APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(scorer_edge::l2dc PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libl2dc.so"
  IMPORTED_SONAME_RELEASE "libl2dc.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS scorer_edge::l2dc )
list(APPEND _IMPORT_CHECK_FILES_FOR_scorer_edge::l2dc "${_IMPORT_PREFIX}/lib/libl2dc.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
