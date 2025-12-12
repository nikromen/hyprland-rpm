%global forgeurl https://github.com/stephenberry/glaze
Version:        6.2.0
%forgemeta

Name:           glaze
Release:        %autorelease
Summary:        Extremely fast, in memory, JSON and reflection library for modern C++

License:        MIT
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  cmake
BuildRequires:  gcc-c++

BuildArch:      noarch


%description
Glaze is one of the fastest JSON libraries in the world. Glaze reads and writes
from object memory, simplifying interfaces and offering incredible performance.


%package        devel
Summary:        Development files for %{name}
BuildArch:      noarch
Provides:       %{name}-static = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%forgeautosetup -p1


%build
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -Dglaze_BUILD_EXAMPLES=OFF \
    -Dglaze_DEVELOPER_MODE=OFF
%cmake_build


%install
%cmake_install


%files devel
%license LICENSE
%doc README.md
%{_includedir}/glaze/
%{_datadir}/glaze/


%changelog
%autochangelog
