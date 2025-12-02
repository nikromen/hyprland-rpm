%global forgeurl https://github.com/hyprwm/hyprcursor
Version:        0.1.13
%forgemeta

Name:           hyprcursor
Release:        %autorelease
Summary:        Hyprland cursor format, library and utilities

License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(tomlplusplus)

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}


%description
The hyprland cursor format, library and utilities.

Hyprcursor is an efficient cursor theme format that fixes XCursor limitations:
- Automatic scaling according to configurable, per-cursor methods
- Support for SVG cursors
- Way more space-efficient than XCursor


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%forgeautosetup -p1


%build
%cmake -DBUILD_TESTING=ON
%cmake_build


%install
%cmake_install


# TODO: fix tests
# %%check
# %%ctest


%files
%license LICENSE
%doc README.md
%{_bindir}/hyprcursor-util
%{_libdir}/libhyprcursor.so.0
%{_libdir}/libhyprcursor.so.%{version}

%files devel
%{_includedir}/hyprcursor.hpp
%{_includedir}/hyprcursor/
%{_libdir}/libhyprcursor.so
%{_libdir}/pkgconfig/hyprcursor.pc


%changelog
%autochangelog
