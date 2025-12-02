%global forgeurl https://github.com/hyprwm/hyprsunset
Version:        0.3.3
%forgemeta

Name:           hyprsunset
Release:        %autorelease
Summary:        An application to enable a blue-light filter on Hyprland

License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprwayland-scanner)
BuildRequires:  pkgconfig(hyprland-protocols)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}


%description
%{summary}.

This utility relies on support for hyprland-ctm-control-v1 by the compositor,
so it's hyprland-exclusive.


%prep
%forgeautosetup -p1


%build
%cmake
%cmake_build


%install
%cmake_install


%post
%systemd_user_post hyprsunset.service

%preun
%systemd_user_preun hyprsunset.service

%postun
%systemd_user_postun_with_restart hyprsunset.service


%files
%license LICENSE
%doc README.md
%{_bindir}/hyprsunset
%{_userunitdir}/hyprsunset.service


%changelog
%autochangelog
