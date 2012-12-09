# TODO
# - pldize initscript
# - finish deps
#
# Conditional build:
%bcond_with	munge		# For MUNGE authentication support.

Summary:	I/O forwarding server for 9P
Name:		diod
Version:	1.0.14
Release:	0.2
License:	GPL v2
Group:		Applications/System
Source0:	https://github.com/chaos/diod/archive/master.tar.gz?/%{name}-%{version}.tgz
# Source0-md5:	1cbe87a0d9b1280f49695789c44a2d22
URL:		http://code.google.com/p/diod/
#BuildRequires:	gperftools-devel
BuildRequires:	libcap-devel
BuildRequires:	libibverbs-devel
BuildRequires:	librdmacm-devel
BuildRequires:	libwrap-devel
BuildRequires:	lua-devel
%{?with_munge:BuildRequires:	munge-devel}
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
diod is a 9P server used in combination with the kernel v9fs file
system for I/O forwarding on Linux clusters.

%prep
%setup -qc
mv %{name}-*/* .

%build
CPPFLAGS="-I/usr/include/ncurses"
%configure \
	--with-tcmalloc
%{__make}

%if %{with tests}
%{__make} check \
	CFLAGS="-Werror %{rpmcflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
mv $RPM_BUILD_ROOT/etc/init.d/* $RPM_BUILD_ROOT/etc/rc.d/init.d

# Kludge to install diodmount as a mount helper.
install -d $RPM_BUILD_ROOT/sbin
mv $RPM_BUILD_ROOT%{_sbindir}/diodmount \
   $RPM_BUILD_ROOT/sbin/mount.diod
mv $RPM_BUILD_ROOT%{_mandir}/man8/diodmount.8 \
   $RPM_BUILD_ROOT%{_mandir}/man8/mount.diod.8

%clean
rm -rf ${RPM_BUILD_ROOT}

%if 0
%post
/sbin/chkconfig --add diod

%preun
if [ "$1" = 0 ]; then
	/sbin/chkconfig --del diod
	%service diod stop
fi
%endif

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog DISCLAIMER.LLNS META NEWS README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/auto.diod
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/diod.conf
%attr(754,root,root) /etc/rc.d/init.d/diod
%attr(755,root,root) /sbin/mount.diod
%attr(755,root,root) %{_sbindir}/diod
%attr(755,root,root) %{_sbindir}/diodcat
%attr(755,root,root) %{_sbindir}/diodload
%attr(755,root,root) %{_sbindir}/diodls
%attr(755,root,root) %{_sbindir}/diodshowmount
%attr(755,root,root) %{_sbindir}/dtop
%{_mandir}/man5/diod.conf.5*
%{_mandir}/man8/diod.8*
%{_mandir}/man8/diodcat.8*
%{_mandir}/man8/diodload.8*
%{_mandir}/man8/diodls.8*
%{_mandir}/man8/diodshowmount.8*
%{_mandir}/man8/dtop.8*
%{_mandir}/man8/mount.diod.8*
