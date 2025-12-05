%global forgeurl https://github.com/hyprwm/hyprpolkitagent
Version:        0.1.3
%forgemeta

Name:           hyprpolkitagent
Release:        %autorelease
Summary:        Simple polkit authentication agent for Hyprland

License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  systemd-rpm-macros
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6QuickControls2)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(polkit-qt6-1)

Requires:       polkit

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}


%description
A simple polkit authentication agent for Hyprland, written in QT/QML.

This package provides a lightweight and Hyprland-integrated way to handle
polkit authentication prompts in a Wayland environment.


%prep
%forgeautosetup -p1


%build
%cmake
%cmake_build


%install
%cmake_install


%post
%systemd_user_post hyprpolkitagent.service

%preun
%systemd_user_preun hyprpolkitagent.service

%postun
%systemd_user_postun_with_restart hyprpolkitagent.service


%files
%license LICENSE
%doc README.md
%{_libexecdir}/hyprpolkitagent
%{_userunitdir}/hyprpolkitagent.service
%{_datadir}/dbus-1/services/org.hyprland.hyprpolkitagent.service


%changelog
%autochangelog
