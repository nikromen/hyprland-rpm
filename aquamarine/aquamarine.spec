%global forgeurl https://github.com/hyprwm/aquamarine
Version:        0.10.0
%forgemeta

Name:           aquamarine
Release:        %autorelease
Summary:        Aquamarine is a very light linux rendering backend library
License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprwayland-scanner)
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)

%description
Aquamarine is a very light linux rendering backend library. It provides basic abstractions for
an application to render on a Wayland session (in a window) or a native DRM session.

It is agnostic of the rendering API (Vulkan/OpenGL) and designed to be
lightweight, performant, and minimal.

Aquamarine provides no bindings for other languages. It is C++-only.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       hyprutils-devel%{?_isa}
Requires:       libdrm-devel%{?_isa}
Requires:       mesa-libEGL-devel%{?_isa}
Requires:       mesa-libgbm-devel%{?_isa}
Requires:       pixman-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%forgeautosetup -p1


%build
%cmake
%cmake_build


%install
%cmake_install


# TODO: make test work
# %%check
# %%ctest


%files
%license LICENSE
%doc README.md
%{_libdir}/libaquamarine.so.9
%{_libdir}/libaquamarine.so.%{version}


%files devel
%{_includedir}/aquamarine/
%{_libdir}/libaquamarine.so
%{_libdir}/pkgconfig/aquamarine.pc


%changelog
%autochangelog
