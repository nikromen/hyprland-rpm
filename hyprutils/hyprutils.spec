%global forgeurl https://github.com/hyprwm/hyprutils
Version:        0.11.0
%forgemeta

Name:           hyprutils
Release:        %autorelease
Summary:        Small C++ library for utilities used across the Hypr* ecosystem
License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  gtest-devel

%description
%{summary}.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pixman-devel%{?_isa}

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


%check
%ctest


%files
%license LICENSE
%doc README.md
%{_libdir}/libhyprutils.so.9
%{_libdir}/libhyprutils.so.%{version}


%files devel
%{_includedir}/hyprutils/
%{_libdir}/libhyprutils.so
%{_libdir}/pkgconfig/hyprutils.pc


%changelog
%autochangelog
