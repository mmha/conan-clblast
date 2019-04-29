# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class ClblastConan(ConanFile):
    name = "clblast"
    version = "1.5.0"
    description = "Tuned OpenCL BLAS"
    topics = ("blas", "opencl", "blas-libraries", "clblas", "matrix-multiplication", "gemm", "gpu")
    url = "https://github.com/bincrafters/conan-clblast"
    homepage = "https://github.com/CNugteren/CLBlast"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "Apache-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "0001-Add-dl-and-pthread-to-required-OpenCL-libs.patch"]
    generators = "cmake"
    requires = "khronos-opencl-headers/[>=20190412]@bincrafters/stable", "khronos-opencl-icd-loader/[>=20190412]@bincrafters/stable"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/CNugteren/CLBlast"
        checksum = "b3198d84d175fd18b0674c0c36f5fb8b7c61a00662afb8596eb5b0b9ab98630c"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version), sha256=checksum)
        extracted_dir = "CLBlast-" + self.version

        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        tools.patch(base_path=self._source_subfolder, patch_file="0001-Add-dl-and-pthread-to-required-OpenCL-libs.patch")
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
