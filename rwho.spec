Summary: Logged in to local network machines
Name: rwho
Version: 0.17
Release: %mkrel 16
License: BSD
Group: Monitoring
Source: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-rwho-%{version}.tar.bz2
Source1: rwhod.init
Url: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/

#FIX for http://www.mandriva.com/security/advisories?name=MDKSA-2005:039
Patch5: rwho-0.17-CAN-2004-1180.patch
#Patch0: netkit-rwho-0.15-alpha.patch
Patch1: netkit-rwho-0.17-bug22014.patch
Patch2: rwho-0.17-fixbcast.patch
Patch3: rwho-0.17-fixhostname.patch

Buildroot: %{_tmppath}/%{name}-%{version}-buildroot
Requires(pre): rpm-helper

%description
The rwho command displays output similar to the output of the who
command (it shows who is logged in) for all machines on the local
network running the rwho daemon.

Install the rwho command if you need to keep track of the users who
are logged in to your local network.

%prep
%setup -q -n netkit-rwho-%{version}

%patch5 -p1 -b .can-2004-118
# (02/11/05 - vdanen) drop due to it being too intrusive against the security patch
# and we don't support alpha anyways
#%patch0 -p1 -b .alpha
%patch1 -p1 -b .bug22014
%patch2 -p0 -b .fixbcast
%patch3 -p1 -b .fixhostname

%build
%serverbuild
CFLAGS="$RPM_OPT_FLAGS" ./configure --with-c-compiler=gcc

make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" -C ruptime

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man{1,8}
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT/var/spool/rwho

make INSTALLROOT=$RPM_BUILD_ROOT MANDIR=%{_mandir} install 
make INSTALLROOT=$RPM_BUILD_ROOT install -C ruptime MANDIR=%{_mandir}

install -m 755 %SOURCE1 $RPM_BUILD_ROOT%{_initrddir}/rwhod

perl -pi -e "s|/etc/rc.d/init.d|%{_initrddir}|" $RPM_BUILD_ROOT%{_initrddir}/*
%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service rwhod

%preun
%_preun_service rwhod

%files
%defattr(-,root,root)
%{_bindir}/ruptime
%{_mandir}/man1/ruptime.1*
%{_bindir}/rwho
%{_mandir}/man1/rwho.1*
%{_sbindir}/rwhod
%{_mandir}/man8/rwhod.8*
%attr(0755,daemon,daemon) /var/spool/rwho
%config(noreplace) %{_initrddir}/rwhod
