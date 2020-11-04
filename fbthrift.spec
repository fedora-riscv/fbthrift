## Depends on fizz, which has linking issues on some platforms:
# https://bugzilla.redhat.com/show_bug.cgi?id=1893332
%ifarch i686 x86_64
%bcond_without static
%else
%bcond_with static
%endif

%global _static_builddir static_build

Name:           fbthrift
Version:        2020.11.02.00
Release:        3%{?dist}
Summary:        Facebook's branch of Apache Thrift, including a new C++ server

License:        ASL 2.0
URL:            https://github.com/facebook/fbthrift
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         %{url}/commit/54dc36c450a09d5f41c0bc31b59247063ed30ed2.patch#/%{name}-%{version}-fuse_protocol_thriftprotocol.patch
Patch1:         %{name}-%{version}-fix_undefined_symbols.patch

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
BuildRequires:  python3-six
BuildRequires:  wangle-devel
%if %{with static}
BuildRequires:  fizz-static
BuildRequires:  folly-static
BuildRequires:  wangle-static
%endif

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


%if %{with static}
%package        static
Summary:        Static development libraries for %{name}
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

%if %{with static}
%files static
%{_libdir}/*.a
%{_libdir}/cmake/%{name}-static
%endif


%changelog
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
