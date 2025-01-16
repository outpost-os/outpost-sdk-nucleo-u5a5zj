import os
from conan import ConanFile
from conan.tools.files import copy
from conan.tools.scm import Git
from conan.tools.gnu import PkgConfig


class outpostSdkRecipe(ConanFile):
    name = "outpost-sdk-nucleo-u5a5zj"
    settings = "os", "arch"
    user = "outpost-os"
    description = """This is the pre-build Outpost SDK for nucleo-u5a5zj board
                  A complete set of tools, headers and pre-built arm-none-eabi binaries
                  for the official STM32 nucleo board"""
    topics = ("outpost","sdk")
    homepage = "https://github.com/outpost-os"
    url = "https://github.com/outpost-os/outpost-sdk-nucleo-u5a5zj"

    def set_version(self):
        git = Git(self)
        try:
            tag = git.run("describe --tags")
            self.version = tag
        except:
            self.version = "nightly"

    def layout(self):
        _os = str(self.settings.os).lower()
        _arch = str(self.settings.arch).lower()
        self.folders.build = os.path.join("output", "staging")
        self.folders.source = os.path.join("output", "src")
        self.cpp.source.includedirs = ["usr/local/include"]
        self.cpp.build.libdirs = ["usr/local/lib"]
        self.cpp.build.bindirs = ["usr/local/bin"]
        self.cpp_info.resdirs = ["usr/local/share"]
        self.cpp_info.srcdirs = ["."]

    def package(self):
        local_include_folder = os.path.join(self.source_folder, self.cpp.source.includedirs[0])
        local_lib_folder = os.path.join(self.build_folder, self.cpp.build.libdirs[0])
        local_bin_folder = os.path.join(self.build_folder, self.cpp.build.bindirs[0])
        local_res_folder = os.path.join(self.build_folder, self.cpp_info.resdirs[0])
        local_src_folder = os.path.join(self.source_folder, self.cpp_info.srcdirs[0])
        copy(self, "*.h", local_include_folder, os.path.join(self.package_folder, "include"), keep_path=False)
        copy(self, "*.a", local_lib_folder, os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, "*.pc", local_lib_folder, os.path.join(self.package_folder, "lib"), keep_path=True)
        copy(self, "*", local_bin_folder, os.path.join(self.package_folder, "bin"), keep_path=False, excludes=["*.bin","*.hex","*.elf"])
        copy(self, "*", local_res_folder, os.path.join(self.package_folder, "share"), keep_path=True)
        copy(self, "*", local_src_folder, os.path.join(self.package_folder, "src"), keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["uapi", "shield_c_lib"]
        pkg_config_dir = os.path.join(self.cpp.build.libdirs, "pkgconfig")
        pkg_config = PkgConfig(conanfile, "uapi", pkg_config_path=pkg_config_dir)
        pkg_config = PkgConfig(conanfile, "shield", pkg_config_path=pkg_config_dir)
        pkg_config.fill_cpp_info(self.cpp_info, is_system=False, system_libs=["m", "rt"])
