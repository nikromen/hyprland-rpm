# rebuild comment
%global forgeurl https://github.com/hyprwm/Hyprland
Version:        0.54.2
%forgemeta

Name:           hyprland
Release:        %autorelease
Summary:        Hyprland is an independent, highly customizable, dynamic tiling Wayland compositor that doesn't sacrifice on its looks

License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  glaze-static
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(aquamarine)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(hyprcursor)
BuildRequires:  pkgconfig(hyprgraphics)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprland-protocols)
BuildRequires:  pkgconfig(hyprwayland-scanner)
BuildRequires:  pkgconfig(hyprwire)
BuildRequires:  hyprwire-scanner
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(muparser)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(re2)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  udis86-devel

Requires:       hyprland-guiutils
Requires:       xorg-x11-server-Xwayland%{?_isa}

Recommends:     polkit
# In default configuration, kitty is used as terminal. The rest
# can be configured and installed from that terminal.
Recommends:     kitty

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}


%description
Hyprland is a 100%% independent, dynamic tiling Wayland compositor that doesn't
sacrifice on its looks.

Features:
- All of the eyecandy: gradient borders, blur, animations, shadows and more
- Extensive customization options
- 100%% independent: no wlroots, no libweston, no kwin, no mutter
- Custom bezier curves for animations
- Powerful plugin support with built-in plugin manager
- Tearing support for better gaming performance
- Fast and active development
- Fully dynamic workspaces
- Config reloaded instantly upon saving


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        uwsm
Summary:        UWSM (Universal Wayland Session Manager) integration for Hyprland
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       uwsm

%description    uwsm
This package provides UWSM (Universal Wayland Session Manager) integration
for Hyprland, allowing better session management and compatibility with
modern desktop environments.


%package        hyprpm
Summary:        Hyprland plugin manager
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       cmake
Requires:       meson
Requires:       cpio
Requires:       pkgconfig
Requires:       git-core
Requires:       gcc-c++
Requires:       gcc
Requires:       mesa-libGLES-devel
Requires:       glslang-devel

%description    hyprpm
Hyprland plugin manager (hyprpm) allows you to download, build, and install
plugins for Hyprland at runtime. This subpackage contains the hyprpm binary
and all necessary build dependencies for compiling Hyprland plugins.


%prep
%forgeautosetup -p1

%build
export GIT_TAG=v%{version}
export GIT_COMMIT_MESSAGE="tag v%{version} at %{forgeurl} - Fedora %{fedora} RPM"
export GIT_DIRTY=clean

%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DNO_SYSTEMD=OFF \
    -DNO_XWAYLAND=OFF \
    -DNO_UWSM=OFF \
    -DNO_HYPRPM=OFF \
    -DBUILD_TESTING=OFF
%cmake_build


%install
%cmake_install

# TODO: fix tests, but I doubt this will be possible
# %%check
# %%ctest


%files
%license LICENSE
%doc README.md
%config(noreplace) %{_datadir}/hypr/hyprland.conf
%{_bindir}/[Hh]yprland
%{_bindir}/hyprctl
%{_bindir}/start-hyprland
%{_datadir}/hypr/
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
%{_mandir}/man1/[Hh]yprland.1*
%{_mandir}/man1/hyprctl.1*
%{bash_completions_dir}/hypr*
%{fish_completions_dir}/hypr*.fish
%{zsh_completions_dir}/_hypr*

%files devel
%{_includedir}/hyprland/
%{_datadir}/pkgconfig/hyprland.pc

%files uwsm
%{_datadir}/wayland-sessions/hyprland-uwsm.desktop

%files hyprpm
%{_bindir}/hyprpm
%{_datadir}/bash-completion/completions/hyprpm
%{_datadir}/fish/vendor_completions.d/hyprpm.fish
%{_datadir}/zsh/site-functions/_hyprpm


%changelog
%autochangelog
