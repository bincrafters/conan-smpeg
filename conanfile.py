#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, CMake
import os
import shutil
import glob


class SMPEGConan(ConanFile):
    name = "smpeg"
    version = "2.0.0"
    description = "SMPEG is a free MPEG1 video player library with sound support"
    topics = ("conan", "smpeg", "mpeg", "mpeg-1", "multimedia", "audio", "video")
    url = "https://github.com/bincrafters/conan-smpeg"
    homepage = "https://icculus.org/smpeg/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "LGPL-2.0-only"
    exports = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "controls": [True, False]}
    default_options = {"shared": False, "fPIC": True, "controls": False}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    requires = "sdl2/2.0.9@bincrafters/stable"
    generators = ["cmake"]
    exports_sources = ["CMakeLists.txt"]

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://www.libsdl.org/projects/smpeg/release/smpeg2-%s.tar.gz" % self.version
        tools.get(source_url, sha256="979a65b211744a44fa641a9b6e4d64e64a12ff703ae776bafe3c4c4cd85494b3")
        extracted_dir = "smpeg2-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _copy_pkg_config(self, name):
        root = self.deps_cpp_info[name].rootpath
        pc_dirs = [os.path.join(root, 'share', 'pkgconfig'), os.path.join(root, 'lib', 'pkgconfig')]
        for pc_dir in pc_dirs:
            pc_files = glob.glob('%s/*.pc' % pc_dir)
            for pc_name in pc_files:
                new_pc = os.path.join('pkgconfig', os.path.basename(pc_name))
                self.output.warn('copying .pc file [%s]: %s' % (name, os.path.basename(pc_name)))
                shutil.copy(pc_name, new_pc)
                prefix = tools.unix_path(root) if self.settings.os == 'Windows' else root
                tools.replace_prefix_in_pc_file(new_pc, prefix)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        cmake.definitions["CONTROLS"] = self.options.controls
        return cmake

    def build(self):
        tools.replace_in_file(os.path.join(self._source_subfolder, "audio", "MPEGaudio.cpp"),
                              '#include "MPEGaudio.h"',
                              '#include <cstring>\n#include "MPEGaudio.h"')
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = ["smpeg2"]
        self.cpp_info.includedirs.append(os.path.join("include", "smpeg2"))
