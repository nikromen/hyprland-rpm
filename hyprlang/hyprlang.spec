%global forgeurl https://github.com/hyprwm/hyprlang
Version:        0.6.7
%forgemeta

Name:           hyprlang
Release:        %autorelease
Summary:        The official implementation library for the hypr config language
License:        LGPL-3.0-only
URL:            %{forgeurl}
Source0:        %{forgesource}

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(hyprutils)

%description
The hypr configuration language is an extremely efficient, yet easy to work
with, configuration language for linux applications.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       hyprutils-devel%{?_isa}

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


%check
%ctest


%files
%license LICENSE
%license COPYRIGHT
%doc README.md
%{_libdir}/libhyprlang.so.2
%{_libdir}/libhyprlang.so.%{version}


%files devel
%{_includedir}/hyprlang.hpp
%{_libdir}/libhyprlang.so
%{_libdir}/pkgconfig/hyprlang.pc


%changelog
%autochangelog
