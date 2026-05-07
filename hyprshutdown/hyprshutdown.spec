%global forgeurl https://github.com/hyprwm/hyprshutdown
Version:        0.1.0
%forgemeta

Name:           hyprshutdown
Release:        %autorelease
Summary:        A graceful shutdown utility for Hyprland

License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  glaze-devel
BuildRequires:  pkgconfig(hyprtoolkit)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pixman-1)

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}


%description
A graceful shutdown/logout utility for Hyprland, which prevents apps
from crashing or dying unexpectedly. It closes all apps and exits
Hyprland cleanly.


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
%{_bindir}/hyprshutdown


%changelog
%autochangelog
