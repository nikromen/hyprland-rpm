%global forgeurl https://codeberg.org/LGFae/awww
Version:        0.11.2
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
install -Dpm 0755 target/rpm/swww %{buildroot}%{_bindir}/swww
install -Dpm 0755 target/rpm/swww-daemon %{buildroot}%{_bindir}/swww-daemon

# Install man pages
install -Dpm 0644 doc/generated/swww.1 %{buildroot}%{_mandir}/man1/swww.1
install -Dpm 0644 doc/generated/swww-daemon.1 %{buildroot}%{_mandir}/man1/swww-daemon.1

# Install shell completions
install -Dpm 0644 completions/swww.bash %{buildroot}%{_datadir}/bash-completion/completions/swww
install -Dpm 0644 completions/swww.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/swww.fish
install -Dpm 0644 completions/_swww %{buildroot}%{_datadir}/zsh/site-functions/_swww
install -Dpm 0644 completions/swww.elv %{buildroot}%{_datadir}/elvish/lib/swww.elv


%check
%cargo_test


%files
%license LICENSE
%license LICENSE.dependencies
%doc README.md CHANGELOG.md
%{_bindir}/swww
%{_bindir}/swww-daemon
%{_mandir}/man1/swww.1*
%{_mandir}/man1/swww-daemon.1*
%{_datadir}/bash-completion/completions/swww
%{_datadir}/fish/vendor_completions.d/swww.fish
%{_datadir}/zsh/site-functions/_swww
%{_datadir}/elvish/lib/swww.elv


%changelog
%autochangelog
