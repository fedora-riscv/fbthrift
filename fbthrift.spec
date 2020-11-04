Name:           fbthrift
Version:        2020.11.02.00
Release:        1%{?dist}
Summary:        Facebook's branch of Apache Thrift, including a new C++ server

License:        ASL 2.0
URL:            https://github.com/facebook/fbthrift
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         %{name}-%{version}-fix_undefined_symbols.patch

# Folly is known not to work on big-endian CPUs
# will add bz# after review
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


%prep
%autosetup -p1


%build
%cmake \
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name} \
  -DCMAKE_SKIP_INSTALL_RPATH=TRUE \
  -DPACKAGE_VERSION=%{version} \
  -Denable_tests=ON
%cmake_build


%install
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


%changelog
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
