Summary:	Little utility will cool your processor
Summary(pl):	Ma貫 narz璠zie, kt鏎e b璠zie ch這dzi這 tw鎩 procesor
Name:		lvcool
Version:	1.7
Release:	2
License:	GPL v2
Group:		Daemons
Source0:	http://vcool.occludo.net/VCool-%{version}-Linux.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-fork.patch
Patch2:		%{name}-sched_yield.patch
URL:		http://vcool.occludo.net/VC_Linux.html
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LVCool will cool your Athlon/Duron processor by switching it to a
low-power mode on Via KT133 or KX133 (VT8363 or VT8371/VT82C686x)
chipsets during idle.

%description -l pl
LVCool och這dzi tw鎩 procesor poprzez prze陰czenie go do trybu o
niskim poborze mocy na chipsetach KT133 lub KX133 (VT8363 lub
VT8371/VT82C686x) podczas stanu ja這wego.

%prep
%setup  -q -n LVCool
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} CC="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{usr/sbin,etc/rc.d/init.d}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/lvcool

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add lvcool
if [ -f /var/lock/subsys/lvcool ]; then
	/etc/rc.d/init.d/lvcool restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/lvcool start\" to start lvcool daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/lvcool ]; then
		/etc/rc.d/init.d/lvcool stop 1>&2
	fi
	/sbin/chkconfig --del lvcool
fi


%files
%defattr(644,root,root,755)
%attr(754,root,root) %{_sbindir}/%{name}
%attr(754,root,root) /etc/rc.d/init.d/lvcool
