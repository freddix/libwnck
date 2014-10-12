Summary:	General Window Manager interfacing for GNOME utilities
Name:		libwnck
Version:	3.4.9
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/libwnck/3.4/%{name}-%{version}.tar.xz
# Source0-md5:	5cb080285e8d5d6a70424cfb43bbf440
Patch0:		%{name}-link.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+3-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	startup-notification-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
General Window Manager interfacing for GNOME utilities. This library
is a part of the GNOME platform.

%package devel
Summary:	Header files and documentation for libwnck
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header, docs and development libraries for libwnck.

%package apidocs
Summary:	libwnck API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libwnck API documentation.

%prep
%setup -q
%patch0 -p1

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules	\
	--disable-static	\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name}-3.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files -f %{name}-3.0.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/wnck-urgency-monitor
%attr(755,root,root) %{_bindir}/wnckprop
%attr(755,root,root) %ghost %{_libdir}/libwnck-3.so.?
%attr(755,root,root) %{_libdir}/libwnck-3.so.*.*.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwnck-3.so
%{_includedir}/%{name}-3.0
%{_pkgconfigdir}/libwnck-3.0.pc
%{_datadir}/gir-1.0/Wnck-3.0.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}-3.0

