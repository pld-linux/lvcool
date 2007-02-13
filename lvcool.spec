Summary:	Little utility will cool your processor
Summary(pl.UTF-8):	Małe narzędzie, które będzie chłodziło twój procesor
Name:		lvcool
Version:	1.7
Release:	3
License:	GPL v2
Group:		Daemons
Source0:	http://vcool.occludo.net/VCool-%{version}-Linux.tar.gz
# Source0-md5:	b07bd25ccc292235783d4890b6be3906
Source1:	%{name}.init
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-fork.patch
Patch2:		%{name}-sched_yield.patch
URL:		http://vcool.occludo.net/VC_Linux.html
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LVCool will cool your Athlon/Duron processor by switching it to a
low-power mode on Via KT133 or KX133 (VT8363 or VT8371/VT82C686x)
chipsets during idle.

%description -l pl.UTF-8
LVCool chłodzi procesor poprzez przełączenie go w tryb o niskim
poborze mocy na chipsetach KT133 lub KX133 (VT8363 lub
VT8371/VT82C686x) podczas stanu jałowego.

%prep
%setup  -q -n LVCool
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} \
	CC="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/lvcool

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add lvcool
%service lvcool restart "lvcool daemon"

%preun
if [ "$1" = "0" ]; then
	%service lvcool stop
	/sbin/chkconfig --del lvcool
fi


%files
%defattr(644,root,root,755)
%attr(754,root,root) %{_sbindir}/%{name}
%attr(754,root,root) /etc/rc.d/init.d/lvcool
