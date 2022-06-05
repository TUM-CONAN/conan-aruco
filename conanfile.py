from conans import ConanFile, tools, CMake
import functools
import os

required_conan_version = ">=1.36.0"


class ArucoConan(ConanFile):
    name = "aruco"
    _version = "3.1.15"
    _revision = ""
    version = _version + _revision

    description = "Augmented reality library based on OpenCV "
    topics = ("aruco", "augmented reality")
    url = "https://github.com/TUM-CONAN/conan-aruco"
    homepage = "https://www.uco.es/investiga/grupos/ava/node/26"
    license = "GPL-3.0-only"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [False, True],
        "fPIC": [False, True],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
    }

    exports_sources = "CMakeLists.txt"
    generators = "cmake", "cmake_find_package"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

        if self.options.shared:
            self.options['opencv'].shared = True

    def requirements(self):
        self.requires("opencv/4.5.0@camposs/stable")
        self.requires("eigen/3.3.9@camposs/stable")

    def source(self):
        tools.get("https://downloads.sourceforge.net/project/aruco/{0}/{0}.zip".format(self.version),
                  destination=self._source_subfolder, strip_root=True)

    @functools.lru_cache(1)
    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ARUCO_DEVINSTALL"] = True
        cmake.definitions["BUILD_TESTS"] = False
        cmake.definitions["BUILD_GLSAMPLES"] = False
        cmake.definitions["BUILD_UTILS"] = False
        cmake.definitions["BUILD_DEBPACKAGE"] = False
        cmake.definitions["BUILD_SVM"] = False
        cmake.definitions["INSTALL_DOC"] = False
        cmake.definitions["USE_OWN_EIGEN3"] = True
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def _patch_for_opencv45(self):
        tools.replace_in_file(os.path.join(self._source_subfolder, "cmake", "findDependencies.cmake"), 
            """find_package(OpenCV REQUIRED)
include_directories( ${OpenCV_INCLUDE_DIRS} )""",
            """set(OpenCV_INCLUDE_DIRS "${CONAN_INCLUDE_DIRS_OPENCV}/opencv4")
include_directories( ${OpenCV_INCLUDE_DIRS} )""")


    def build(self):
        self._patch_for_opencv45()
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        tools.rmdir(os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.set_property("pkg_config_name", "aruco")
        self.cpp_info.includedirs.append(os.path.join("include", "aruco"))
        self.cpp_info.libs = tools.collect_libs(self)


