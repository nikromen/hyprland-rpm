%global forgeurl https://github.com/hyprwm/hyprland-protocols
Version:        0.7.0
%forgemeta

Name:           hyprland-protocols
Release:        %autorelease
Summary:        Wayland protocol extensions for Hyprland

License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson

BuildArch:      noarch


%description
Wayland protocol extensions for Hyprland.

This repository exists in an effort to bridge the gap between Hyprland and
KDE/Gnome's functionality, as well as allow apps for some extra neat
functionality under Hyprland.

Since wayland-protocols is slow to change (on top of Hyprland not being
allowed to contribute), we have to maintain a set of protocols Hyprland uses
to plumb some things / add some useful features.


%prep
%forgeautosetup -p1


%build
%meson
%meson_build


%install
%meson_install


%files
%license LICENSE
%doc README.md
%{_datadir}/hyprland-protocols/
%{_datadir}/pkgconfig/hyprland-protocols.pc


%changelog
%autochangelog
