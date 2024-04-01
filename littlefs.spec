#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Little fail-safe filesystem designed for microcontrollers
Summary(pl.UTF-8):	Mały, odporny na awarie zasilania system plików dla mikrokontrolerów
Name:		littlefs
Version:	2.9.1
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/littlefs-project/littlefs/releases
Source0:	https://github.com/littlefs-project/littlefs/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a870347a97de9b3f909bc5b45e6fb886
URL:		https://github.com/littlefs-project/littlefs
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Little fail-safe filesystem designed for microcontrollers.

%description -l pl.UTF-8
Mały, odporny na awarie zasilania system plików zaprojektowany z myślą
o mikrokontrolerach.

%package devel
Summary:	Header files for littlefs library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki littlefs
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for littlefs library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki littlefs.

%package static
Summary:	Static littlefs library
Summary(pl.UTF-8):	Statyczna biblioteka littlefs
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static littlefs library.

%description static -l pl.UTF-8
Statyczna biblioteka littlefs.

%prep
%setup -q

%build
libtool --mode=compile %{__cc} %{rpmcflags} %{rpmcppflags} -Wall -Wextra -pedantic -Wmissing-prototypes -c lfs.c -o lfs.lo
libtool --mode=compile %{__cc} %{rpmcflags} %{rpmcppflags} -Wall -Wextra -pedantic -Wmissing-prototypes -c lfs_util.c -o lfs_util.lo
libtool --mode=compile %{__cc} %{rpmcflags} %{rpmcppflags} -Wall -Wextra -pedantic -Wmissing-prototypes -c bd/lfs_filebd.c -o lfs_filebd.lo
libtool --mode=compile %{__cc} %{rpmcflags} %{rpmcppflags} -Wall -Wextra -pedantic -Wmissing-prototypes -c bd/lfs_rambd.c -o lfs_rambd.lo
libtool --mode=link %{__cc} %{!?with_static_libs:-shared} %{rpmldflags} %{rpmcflags} -o liblfs.la lfs.lo lfs_util.lo lfs_filebd.lo lfs_rambd.lo -rpath %{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir}}

cp -p lfs.h lfs_util.h bd/lfs_filebd.h bd/lfs_rambd.h $RPM_BUILD_ROOT%{_includedir}

libtool --mode=install install liblfs.la $RPM_BUILD_ROOT%{_libdir}

# no external dependencies
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblfs.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc DESIGN.md LICENSE.md README.md SPEC.md
%attr(755,root,root) %{_libdir}/liblfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblfs.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblfs.so
%{_includedir}/lfs.h
%{_includedir}/lfs_filebd.h
%{_includedir}/lfs_rambd.h
%{_includedir}/lfs_util.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/liblfs.a
%endif
