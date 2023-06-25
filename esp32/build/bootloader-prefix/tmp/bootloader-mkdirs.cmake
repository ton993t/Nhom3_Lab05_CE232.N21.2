# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "C:/Users/duyhu/esp/esp-idf/components/bootloader/subproject"
  "D:/Lab/WirelessEmbedded/Mini-Project/build/bootloader"
  "D:/Lab/WirelessEmbedded/Mini-Project/build/bootloader-prefix"
  "D:/Lab/WirelessEmbedded/Mini-Project/build/bootloader-prefix/tmp"
  "D:/Lab/WirelessEmbedded/Mini-Project/build/bootloader-prefix/src/bootloader-stamp"
  "D:/Lab/WirelessEmbedded/Mini-Project/build/bootloader-prefix/src"
  "D:/Lab/WirelessEmbedded/Mini-Project/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "D:/Lab/WirelessEmbedded/Mini-Project/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "D:/Lab/WirelessEmbedded/Mini-Project/build/bootloader-prefix/src/bootloader-stamp${cfgdir}") # cfgdir has leading slash
endif()
