%global forgeurl https://github.com/hyprwm/hyprpicker
Version:        0.4.5
%forgemeta

Name:           hyprpicker
Release:        %autorelease
Summary:        A wlroots-compatible Wayland color picker

License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprwayland-scanner)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}


%description
%{summary}.


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
%{_bindir}/hyprpicker
%{_mandir}/man1/hyprpicker.1*


%changelog
%autochangelog
