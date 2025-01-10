import os
from conan import ConanFile
from conan.tools.files import copy
from conan.tools.scm import Git


class outpostSdkRecipe(ConanFile):
    name = "outpost-sdk-u5a5zj"
    settings = "os", "arch"

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
        self.folders.source = self.folders.build
        self.cpp.source.includedirs = ["usr/local/include"]
        self.cpp.build.libdirs = ["usr/local/lib"]
        self.cpp.build.bindirs = ["usr/local/bin"]
        self.cpp_info.resdirs = ["usr/local/share"]

    def package(self):
        local_include_folder = os.path.join(self.source_folder, self.cpp.source.includedirs[0])
        local_lib_folder = os.path.join(self.build_folder, self.cpp.build.libdirs[0])
        local_bin_folder = os.path.join(self.build_folder, self.cpp.build.bindirs[0])
        local_res_folder = os.path.join(self.build_folder, self.cpp_info.resdirs[0])
        copy(self, "*.h", local_include_folder, os.path.join(self.package_folder, "include"), keep_path=False)
        copy(self, "*.a", local_lib_folder, os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, "*.pc", local_lib_folder, os.path.join(self.package_folder, "lib"), keep_path=True)
        copy(self, "*.elf", local_bin_folder, os.path.join(self.package_folder, "bin"), keep_path=False)
        copy(self, "*.hex", local_bin_folder, os.path.join(self.package_folder, "bin"), keep_path=False)
        copy(self, "*.bin", local_bin_folder, os.path.join(self.package_folder, "bin"), keep_path=False)
        copy(self, "*", local_res_folder, os.path.join(self.package_folder, "share"), keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["uapi"]
