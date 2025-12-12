%global forgeurl https://github.com/hyprwm/hyprtoolkit
Version:        0.4.1
%forgemeta

Name:           hyprtoolkit
Release:        %autorelease
Summary:        Modern C++ Wayland-native GUI toolkit
License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  hyprwayland-scanner
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  pkgconfig(hyprgraphics)
BuildRequires:  pkgconfig(aquamarine)
BuildRequires:  mesa-libGLES-devel

%description
A modern C++ Wayland-native GUI toolkit designed to be small, simple,
and modern for making Wayland GUI applications with smooth animations,
easy usage, and simple system theming.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       hyprwayland-scanner
Requires:       hyprutils-devel%{?_isa}
Requires:       hyprlang-devel%{?_isa}
Requires:       hyprgraphics-devel%{?_isa}
Requires:       aquamarine-devel%{?_isa}

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


%files
%license LICENSE
%doc README.md
%{_libdir}/libhyprtoolkit.so.4
%{_libdir}/libhyprtoolkit.so.%{version}


%files devel
%{_includedir}/hyprtoolkit/
%{_libdir}/libhyprtoolkit.so
%{_libdir}/pkgconfig/hyprtoolkit.pc


%changelog
%autochangelog
