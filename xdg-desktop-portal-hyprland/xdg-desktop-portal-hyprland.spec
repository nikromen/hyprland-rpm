%global forgeurl https://github.com/hyprwm/xdg-desktop-portal-hyprland
Version:        1.3.11
%forgemeta

Name:           xdg-desktop-portal-hyprland
Release:        %autorelease
Summary:        XDG Desktop Portal backend for Hyprland

License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprland-protocols)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprwayland-scanner)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libspa-0.2)
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6Gui)
BuildRequires:  pkgconfig(Qt6Qml)
BuildRequires:  pkgconfig(Qt6Quick)
BuildRequires:  pkgconfig(Qt6WaylandClient)
BuildRequires:  pkgconfig(Qt6Widgets)
BuildRequires:  pkgconfig(sdbus-c++)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)

Requires:       dbus
Requires:       pipewire
Requires:       xdg-desktop-portal

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}


%description
An XDG Desktop Portal backend for Hyprland (and wlroots).

xdg-desktop-portal-hyprland (XDPH) provides screen sharing and other
XDG desktop portal functionality for Hyprland and wlroots-based compositors.


%prep
%forgeautosetup -p1


%build
%cmake -DCMAKE_INSTALL_LIBEXECDIR=%{_libexecdir}
%cmake_build


%install
%cmake_install


%post
%systemd_user_post xdg-desktop-portal-hyprland.service

%preun
%systemd_user_preun xdg-desktop-portal-hyprland.service

%postun
%systemd_user_postun_with_restart xdg-desktop-portal-hyprland.service


%files
%license LICENSE
%doc README.md
%{_libexecdir}/xdg-desktop-portal-hyprland
%{_bindir}/hyprland-share-picker
%{_datadir}/xdg-desktop-portal/portals/hyprland.portal
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.hyprland.service
%{_userunitdir}/xdg-desktop-portal-hyprland.service


%changelog
%autochangelog
