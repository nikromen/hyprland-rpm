%global forgeurl https://github.com/hyprwm/hyprwayland-scanner
Version:        0.4.5
%forgemeta

Name:           hyprwayland-scanner
Release:        %autorelease
Summary:        A Hyprland implementation of wayland-scanner, in and for C++
License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(pugixml)

%description
A Hyprland implementation of wayland-scanner, in and for C++.

hyprwayland-scanner automatically generates properly RAII-ready, modern C++
bindings for Wayland protocols, for either servers or clients.


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
%{_bindir}/hyprwayland-scanner
%{_libdir}/cmake/hyprwayland-scanner/
%{_libdir}/pkgconfig/hyprwayland-scanner.pc


%changelog
%autochangelog
