%global forgeurl https://github.com/hyprwm/hyprwire
Version:        0.3.0
%forgemeta

Name:           hyprwire
Release:        %autorelease
Summary:        A fast and consistent wire protocol for IPC
License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(pugixml)


%description
A fast and consistent wire protocol for IPC used in the Hyprland ecosystem.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        scanner
Summary:        Protocol code generator for %{name}

%description    scanner
The %{name}-scanner package contains the hyprwire-scanner tool
for generating protocol code from XML protocol definitions.


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
%{_libdir}/libhyprwire.so.3
%{_libdir}/libhyprwire.so.%{version}


%files devel
%{_includedir}/hyprwire/
%{_libdir}/libhyprwire.so
%{_libdir}/pkgconfig/hyprwire.pc


%files scanner
%{_bindir}/hyprwire-scanner
%{_libdir}/pkgconfig/hyprwire-scanner.pc
%{_libdir}/cmake/hyprwire-scanner/


%changelog
%autochangelog
