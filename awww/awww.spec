%global forgeurl https://codeberg.org/LGFae/awww
Version:        0.12.1
%global tag v%{version}
%forgemeta

Name:           awww
Release:        %autorelease
Summary:        Efficient animated wallpaper daemon for Wayland, controlled at runtime

License:        GPL-3.0-or-later
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  cargo-rpm-macros
BuildRequires:  gcc
BuildRequires:  scdoc
BuildRequires:  pkgconfig(dav1d)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}


%description
An Answer to your Wayland Wallpaper Woes - Efficient animated wallpaper daemon
for Wayland, controlled at runtime.

Note: This will not work on GNOME as it does not implement the wlr-layer-shell
protocol.


%prep
%forgeautosetup -p1
cargo vendor
%cargo_prep -v vendor


%build
%cargo_build -f avif
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%{cargo_vendor_manifest}

# Generate man pages
./doc/gen.sh


%install
install -Dpm 0755 target/rpm/awww %{buildroot}%{_bindir}/awww
install -Dpm 0755 target/rpm/awww-daemon %{buildroot}%{_bindir}/awww-daemon

# Install man pages
install -Dpm 0644 doc/generated/awww.1 %{buildroot}%{_mandir}/man1/awww.1
install -Dpm 0644 doc/generated/awww-daemon.1 %{buildroot}%{_mandir}/man1/awww-daemon.1
install -Dpm 0644 doc/generated/awww-clear.1 %{buildroot}%{_mandir}/man1/awww-clear.1
install -Dpm 0644 doc/generated/awww-clear-cache.1 %{buildroot}%{_mandir}/man1/awww-clear-cache.1
install -Dpm 0644 doc/generated/awww-img.1 %{buildroot}%{_mandir}/man1/awww-img.1
install -Dpm 0644 doc/generated/awww-kill.1 %{buildroot}%{_mandir}/man1/awww-kill.1
install -Dpm 0644 doc/generated/awww-pause.1 %{buildroot}%{_mandir}/man1/awww-pause.1
install -Dpm 0644 doc/generated/awww-query.1 %{buildroot}%{_mandir}/man1/awww-query.1
install -Dpm 0644 doc/generated/awww-restore.1 %{buildroot}%{_mandir}/man1/awww-restore.1


%check
%cargo_test


%files
%license LICENSE
%license LICENSE.dependencies
%doc README.md CHANGELOG.md
%{_bindir}/awww
%{_bindir}/awww-daemon
%{_mandir}/man1/awww.1*
%{_mandir}/man1/awww-daemon.1*
%{_mandir}/man1/awww-clear.1*
%{_mandir}/man1/awww-clear-cache.1*
%{_mandir}/man1/awww-img.1*
%{_mandir}/man1/awww-kill.1*
%{_mandir}/man1/awww-pause.1*
%{_mandir}/man1/awww-query.1*
%{_mandir}/man1/awww-restore.1*


%changelog
%autochangelog
