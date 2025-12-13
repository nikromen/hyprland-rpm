# rebuild comment
%global forgeurl https://github.com/hyprwm/Hyprland
Version:        0.52.2
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

%description    hyprpm
Hyprland plugin manager (hyprpm) allows you to download, build, and install
plugins for Hyprland at runtime. This subpackage contains the hyprpm binary
and all necessary build dependencies for compiling Hyprland plugins.


%prep
%forgeautosetup -p1

# Create a minimal pkg-config file for udis86 since Fedora doesn't ship one
cat > udis86.pc << 'EOF'
prefix=/usr
exec_prefix=${prefix}
libdir=${exec_prefix}/lib64
includedir=${prefix}/include

Name: udis86
Description: Disassembler Library for x86 and x86-64
Version: 1.7.2
Libs: -L${libdir} -ludis86
Cflags: -I${includedir}
EOF


%build
export PKG_CONFIG_PATH="${PWD}:${PKG_CONFIG_PATH}"
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DNO_SYSTEMD=OFF \
    -DNO_XWAYLAND=OFF \
    -DNO_UWSM=OFF \
    -DNO_HYPRPM=OFF \
    -DUSE_SYSTEM_UDIS86=ON \
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
%{_bindir}/[Hh]yprland
%{_bindir}/hyprctl
%config(noreplace) %{_datadir}/hypr/hyprland.conf
%{_datadir}/bash-completion/completions/hyprctl
%{_datadir}/fish/vendor_completions.d/hyprctl.fish
%{_datadir}/hypr/
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
%{_datadir}/zsh/site-functions/_hyprctl
%{_mandir}/man1/[Hh]yprland.1*
%{_mandir}/man1/hyprctl.1*

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
