Summary:	Logged in to local network machines
Name:		rwho
Version:	0.17
Release:	29
License:	BSD
Group:		Monitoring
Url:		ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/
Source:		ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-rwho-%{version}.tar.bz2
Source1:	rwhod.service
#FIX for http://www.mandriva.com/security/advisories?name=MDKSA-2005:039
Patch0:		netkit-rwho-0.17-makefiles.patch
Patch2:		rwho-0.17-fixbcast.patch
Patch3:		rwho-0.17-fixhostname.patch
Patch5:		rwho-0.17-CAN-2004-1180.patch

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
%patch0 -p1 -b .makefiles
%patch2 -p0 -b .fixbcast
%patch3 -p1 -b .fixhostname

%build
%serverbuild
CFLAGS="%{optflags}" ./configure --with-c-compiler=gcc

make RPM_OPT_FLAGS="%{optflags}"
make RPM_OPT_FLAGS="%{optflags}" -C ruptime

%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}/%{_mandir}/man{1,8}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/var/spool/rwho

make INSTALLROOT=%{buildroot} MANDIR=%{_mandir} install 
make INSTALLROOT=%{buildroot} install -C ruptime MANDIR=%{_mandir}

install -m 755 %{SOURCE1} %{buildroot}%{_unitdir}/rwhod.service

%post
%systemd_post rwhod.service

%preun
%systemd_preun rwhod.service

%postun
%systemd_postun_with_restart rwhod.service

%files
%{_bindir}/ruptime
%{_mandir}/man1/ruptime.1*
%{_bindir}/rwho
%{_mandir}/man1/rwho.1*
%{_sbindir}/rwhod
%{_mandir}/man8/rwhod.8*
%attr(0755,daemon,daemon) /var/spool/rwho
%{_unitdir}/rwhod*

