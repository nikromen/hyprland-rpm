%global forgeurl https://github.com/hyprwm/hypridle
Version:        0.1.7
%forgemeta

Name:           hypridle
Release:        %autorelease
Summary:        Hyprland's idle management daemon

License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprwayland-scanner)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(sdbus-c++)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(hyprland-protocols)

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}


%description
Hypridle is Hyprland's idle management daemon. It is based on the
ext-idle-notify-v1 wayland protocol and supports dbus' loginctl
commands (lock/unlock/before-sleep) as well as dbus' inhibit
(used by e.g. firefox/steam).


%prep
%forgeautosetup -p1


%build
%cmake -DBUILD_TESTING=ON
%cmake_build


%install
%cmake_install


%check
%ctest


%post
%systemd_user_post hypridle.service

%preun
%systemd_user_preun hypridle.service

%postun
%systemd_user_postun_with_restart hypridle.service


%files
%license LICENSE
%doc README.md
%{_bindir}/hypridle
%{_userunitdir}/hypridle.service
%config(noreplace) %{_datadir}/hypr/hypridle.conf


%changelog
%autochangelog
