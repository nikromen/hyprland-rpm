%global forgeurl https://github.com/hyprwm/hyprland-guiutils
Version:        0.2.0
%forgemeta

Name:           hyprland-guiutils
Release:        %autorelease
Summary:        Hyprland GUI utilities
License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprtoolkit)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libdrm)

%description
Hyprland GUI utilities - successor to hyprland-qtutils. Collection of
graphical utilities for the Hyprland compositor.


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
%{_bindir}/hyprland-dialog
%{_bindir}/hyprland-donate-screen
%{_bindir}/hyprland-update-screen
%{_bindir}/hyprland-welcome
%{_bindir}/hyprland-run


%changelog
%autochangelog
