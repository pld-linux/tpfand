Summary:	Controls fan speed of ThinkPad notebooks
Name:		tpfand
Version:	0.94
Release:	0.1
License:	GPL v3
Group:		Daemons
Source0:	http://launchpad.net/tp-fan/tpfand/0.94/+download/%{name}-%{version}.tar.gz
# Source0-md5:	fa08a5c3eebd47842e1fb84b6283416d
URL:		https://launchpad.net/tp-fan
BuildRequires:	perl-tools-pod
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The tpfand daemon controls the system fan of IBM/Lenovo ThinkPad
notebooks in software according to specified temperature profile.

It can be used to make the notebook quieter. However this also results
in higher system temperatures that may damage and/or shorten the
lifespan of your computer.

tpfand-profiles contains contributed temperature profiles. tpfan-admin
provides a graphical configuration and monitoring interface.

%prep
%setup -q

# fix python path
%{__sed} -i -e 's,/usr/lib/python2.5/site-packages,%{py_sitescriptdir},' Makefile

# /etc/modprobe.d must contain *.conf extension
%{__sed} -i -e 's,/etc/modprobe.d/$,&thinkpad_acpi.conf,' Makefile

# our init.d path
%{__sed} -i -e 's,/etc/init.d,/etc/rc.d/init.d,' Makefile

# preserve timestamps
%{__sed} -i -e 's,install ,install -p ,' Makefile

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

rm -rf $RPM_BUILD_ROOT/etc/acpi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
/etc/dbus-1/system.d/tpfand.conf
/etc/modprobe.d/thinkpad_acpi.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/tpfand.conf
%attr(754,root,root) /etc/rc.d/init.d/tpfand
%attr(755,root,root) %{_sbindir}/tpfand
%dir %{_datadir}/tpfand
%dir %{_datadir}/tpfand/models
%{_datadir}/tpfand/models/generic
%dir %{py_sitescriptdir}/tpfand
%{py_sitescriptdir}/tpfand/*.py[co]
