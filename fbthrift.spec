%bcond_without python

## Depends on fizz, which has linking issues on some platforms:
# https://bugzilla.redhat.com/show_bug.cgi?id=1893332
%ifarch i686 x86_64
%bcond_without static
%else
%bcond_with static
%endif

%global _static_builddir static_build

Name:           fbthrift
Version:        2020.11.16.00
Release:        1%{?dist}
Summary:        Facebook's branch of Apache Thrift, including a new C++ server

License:        ASL 2.0
URL:            https://github.com/facebook/fbthrift
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         %{name}-python3-cmake.patch

# Folly is known not to work on big-endian CPUs
# https://bugzilla.redhat.com/show_bug.cgi?id=1894635
ExcludeArch:    s390x

BuildRequires:  cmake
BuildRequires:  gcc-c++
# Tool dependencies
BuildRequires:  bison
BuildRequires:  flex
# Library dependencies
BuildRequires:  fizz-devel
BuildRequires:  folly-devel
BuildRequires:  wangle-devel

%description
Thrift is a serialization and RPC framework for service communication. Thrift
enables these features in all major languages, and there is strong support for
C++, Python, Hack, and Java. Most services at Facebook are written using Thrift
for RPC, and some storage systems use Thrift for serializing records on disk.

Facebook Thrift is not a distribution of Apache Thrift. This is an evolved
internal branch of Thrift that Facebook re-released to open source community in
February 2014. Facebook Thrift was originally released closely tracking Apache
Thrift but is now evolving in new directions. In particular, the compiler was
rewritten from scratch and the new implementation features a fully asynchronous
Thrift server.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Conflicts:      thrift-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%if %{with python}
%package -n python3-%{name}
Summary:        Python bindings for %{name}
BuildRequires:  python3-devel
BuildRequires:  python3-folly-devel
BuildRequires:  python3dist(cython)
BuildRequires:  python3dist(wheel)
Requires:       %{name}%{?_isa} = %{version}-%{release}
Conflicts:      python3-thrift

%description -n python3-%{name}
The python3-%{name} package contains Python bindings for %{name}.


%package -n python3-%{name}-devel
Summary:        Development files for python3-%{name}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       python3-%{name}%{?_isa} = %{version}-%{release}

%description -n python3-%{name}-devel
The python3-%{name}-devel package contains libraries and header files for
developing applications that use python3-%{name}.
%endif


%if %{with static}
%package        static
Summary:        Static development libraries for %{name}
BuildRequires:  fizz-static
BuildRequires:  folly-static
BuildRequires:  wangle-static
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    static
The %{name}-static package contains static libraries for
developing applications that use %{name}.
%endif


%prep
%autosetup -p1


%build
%if %{with static}
# static build
mkdir %{_static_builddir}
pushd %{_static_builddir}
%cmake .. \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name}-static \
  -DPACKAGE_VERSION=%{version} \
  -DFIZZ_ROOT=%{_libdir}/cmake/fizz-static \
  -DFOLLY_ROOT=%{_libdir}/cmake/folly-static \
  -DWANGLE_ROOT=%{_libdir}/cmake/wangle-static \
  -Denable_tests=OFF
%cmake_build
popd

%endif

%cmake \
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name} \
  -DCMAKE_SKIP_INSTALL_RPATH=TRUE \
  -DPACKAGE_VERSION=%{version} \
%if %{with python}
  -Dthriftpy3=ON \
%endif
  -Denable_tests=ON
%cmake_build


%install
%if %{with static}
# static build
pushd %{_static_builddir}
%cmake_install
popd
%endif

%cmake_install

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%check
%ctest


%files
%license LICENSE
%{_bindir}/thrift1
%{_libdir}/*.so.*

%files devel
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md README.md
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/%{name}
%exclude %{_includedir}/thrift/lib/py3

%if %{with python}
%files -n python3-%{name}
%{python3_sitearch}/thrift
%{python3_sitearch}/thrift-0.0.1-py%{python3_version}.egg-info
%exclude %{python3_sitearch}/thrift/py3/*.pxd

%files -n python3-%{name}-devel
%{_includedir}/thrift/lib/py3
%{python3_sitearch}/thrift/*.pxd
%{python3_sitearch}/thrift/py3/*.pxd
%endif

%if %{with static}
%files static
%{_libdir}/*.a
%{_libdir}/cmake/%{name}-static
%endif


%changelog
* Mon Nov 16 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.11.16.00-1
- Update to 2020.11.16.00

* Fri Nov 13 2020 Filipe Brandenburger <filbranden@fb.com> - 2020.11.09.00-3
- Update CMakeList and setup.py for python3 to include all modules and
  to include enums source together with the types module.

* Tue Nov 10 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.11.09.00-2
- Enable Python binding by default

* Mon Nov  9 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.11.09.00-1
- Update to 2020.11.09.00
- Enable Python binding

* Wed Nov  4 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.11.02.00-3
- Rebase patch on top of upstream CMakeLists.txt change

* Wed Nov  4 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.11.02.00-2
- Enable static subpackage on architectures where fizz-static is available

* Mon Nov  2 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.11.02.00-1
- Update to 2020.11.02.00
- Fix undefined symbol warnings

* Mon Nov  2 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.10.26.00-3
- Mark fbthrift-devel as conflicting with thrift-devel
- Disable RPATH when installing libraries

* Thu Oct 29 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.10.26.00-2
- Use shorter, canonical URL for source

* Tue Oct 27 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.10.26.00-1
- Initial package
