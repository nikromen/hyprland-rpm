%global forgeurl https://github.com/hyprwm/hyprgraphics
Version:        0.4.0
%forgemeta

Name:           hyprgraphics
Release:        %autorelease
Summary:        Small C++ library for graphics / resource utilities used across the Hypr* ecosystem

License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(libheif)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libjxl)
BuildRequires:  pkgconfig(libjxl_cms)
BuildRequires:  pkgconfig(libjxl_threads)
BuildRequires:  pkgconfig(libmagic)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)

# ExcludeArch: %{ix86} since C++26 and i686 are being phased out
ExcludeArch:    %{ix86}


%description
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cairo-devel
Requires:       hyprutils-devel
Requires:       libjpeg-devel
Requires:       libpng-devel
Requires:       libwebp-devel
Requires:       pango-devel
Requires:       pixman-devel


%description    devel
Development files for %{name}.


%prep
%forgeautosetup -p1


%build
%cmake -DBUILD_TESTING=ON
%cmake_build


%install
%cmake_install


%check
%ctest


%files
%license LICENSE
%doc README.md
%{_libdir}/libhyprgraphics.so.3
%{_libdir}/libhyprgraphics.so.%{version}


%files devel
%{_includedir}/hyprgraphics/
%{_libdir}/libhyprgraphics.so
%{_libdir}/pkgconfig/hyprgraphics.pc


%changelog
%autochangelog
