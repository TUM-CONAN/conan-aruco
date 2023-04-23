from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout, CMakeDeps
import os


class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "VirtualRunEnv"
    test_type = "explicit"

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires(self.tested_reference_str)
        self.requires("opencv/4.5.5@camposs/stable")

    def generate(self):
        tc = CMakeToolchain(self)
        # opencv_root = self.dependencies["opencv"].package_folder
        # tc.variables["OpenCV_ROOT"] = opencv_root
        tc.generate()

        deps = CMakeDeps(self)
        deps.set_property("opencv", "cmake_find_mode", "module")
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if can_run(self):
            bin_path = os.path.join(self.cpp.build.bindirs[0], "test_package")
            self.run(bin_path, env="conanrun")