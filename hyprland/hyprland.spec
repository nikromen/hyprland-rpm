# rebuild comment
%global forgeurl https://github.com/hyprwm/Hyprland
Version:        0.54.3

# Used both at Hyprland package build time and at
# runtime by hyprpm which compiles plugins from source
%{lua:
hyprland_shared_deps = {
    "cmake",
    "gcc-c++",
    "git-core",
    "glaze-static",
    "hyprwire-scanner",
    "pkgconfig(aquamarine)",
    "pkgconfig(cairo)",
    "pkgconfig(egl)",
    "pkgconfig(gbm)",
    "pkgconfig(gio-2.0)",
    "pkgconfig(gl)",
    "pkgconfig(glesv2)",
    "pkgconfig(hyprcursor)",
    "pkgconfig(hyprgraphics)",
    "pkgconfig(hyprlang)",
    "pkgconfig(hyprland-protocols)",
    "pkgconfig(hyprutils)",
    "pkgconfig(hyprwayland-scanner)",
    "pkgconfig(hyprwire)",
    "pkgconfig(lcms2)",
    "pkgconfig(libdrm)",
    "pkgconfig(libinput)",
    "pkgconfig(muparser)",
    "pkgconfig(pango)",
    "pkgconfig(pangocairo)",
    "pkgconfig(pixman-1)",
    "pkgconfig(re2)",
    "pkgconfig(tomlplusplus)",
    "pkgconfig(uuid)",
    "pkgconfig(wayland-protocols)",
    "pkgconfig(wayland-scanner)",
    "pkgconfig(wayland-server)",
    "pkgconfig(xcb)",
    "pkgconfig(xcb-composite)",
    "pkgconfig(xcb-errors)",
    "pkgconfig(xcb-icccm)",
    "pkgconfig(xcb-render)",
    "pkgconfig(xcb-res)",
    "pkgconfig(xcb-xfixes)",
    "pkgconfig(xcursor)",
    "pkgconfig(xkbcommon)",
}
}

Name:           hyprland
Release:        %autorelease
Summary:        Hyprland is an independent, highly customizable, dynamic tiling Wayland compositor that doesn't sacrifice on its looks

License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgeurl}/releases/download/v%{version}/source-v%{version}.tar.gz

%{lua: for _, d in ipairs(hyprland_shared_deps) do print("BuildRequires:  "..d.."\n") end}
BuildRequires:  systemd-rpm-macros
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
# hyprpm clones Hyprland source and runs cmake to compile plugins, so it needs
# the full set of build dependencies at runtime
%{lua: for _, d in ipairs(hyprland_shared_deps) do print("Requires:       "..d.."\n") end}
Requires:       gcc
Requires:       meson
Requires:       cpio
Requires:       pkgconfig
Requires:       glslang-devel

%description    hyprpm
Hyprland plugin manager (hyprpm) allows you to download, build, and install
plugins for Hyprland at runtime.

Note: This package pulls in a large number of development libraries because
hyprpm compiles Hyprland from source to build plugins. Only install this
package if you intend to use Hyprland plugins.


%prep
%autosetup -n hyprland-source -p1
rm -rf subprojects/udis86
rm -rf subprojects/hyprland-protocols
rm -rf subprojects/tracy

%build
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
