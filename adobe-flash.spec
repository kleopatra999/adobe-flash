#
# Conditional build:
%bcond_with	license_agreement	# generates package
#
%define		_ver_major	9
%define		_ver_minor	0
%define		_ver_patch	31
%define		_ver_serial	0
%define		base_name	macromedia-flash
Summary:	Flash plugin for Netscape-compatible WWW browsers
Summary(pl):	Wtyczka Flash dla przeglądarek WWW zgodnych z Netscape
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
%define		_rel 1
Version:	%{_ver_major}.%{_ver_minor}.%{_ver_patch}.%{_ver_serial}
Release:	%{_rel}%{?with_license_agreement:wla}
License:	Free to use, non-distributable
Group:		X11/Applications/Multimedia
%if %{with license_agreement}
Source0:	http://fpdownload.macromedia.com/get/flashplayer/current/install_flash_player_9_linux.tar.gz
# NoSource0-md5:	76b38231a68995935185aa42dfda9db7
%else
Source0:	license-installer.sh
# NoSource0-md5:	76b38231a68995935185aa42dfda9db7
%endif
URL:		http://www.adobe.com/products/flashplayer/
%if %{with license_agreement}
BuildRequires:	rpmbuild(macros) >= 1.357
Requires:	browser-plugins >= 2.0
%else
Requires:	rpm-build-tools
%endif
Obsoletes:	flash-plugin
Obsoletes:	konqueror-plugin-macromedia-flash
Obsoletes:	mozilla-firefox-plugin-macromedia-flash
Obsoletes:	mozilla-plugin-macromedia-flash
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/adobe

%description
Adobe(R) Flash(R) Player is the high-performance, lightweight, highly expressive
client runtime that delivers powerful and consistent user experiences across
major operating systems, browsers, mobile phones, and devices. Installed on
over 700 million Internet-connected desktops and mobile devices, Flash Player
enables organizations and individuals to build and deliver great digital
experiences to their end users.

%description -l pl
Wtyczka Flash dla przeglądarek WWW zgodnych z Netscape.

%prep
%if %{with license_agreement}
%setup -q -n install_flash_player_%{_ver_major}_linux
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{without license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

sed -e '
	s/@BASE_NAME@/%{base_name}/g
	s/@TARGET_CPU@/%{_target_cpu}/g
	s-@VERSION@-%{version}-g
	s-@RELEASE@-%{release}-g
	s,@SPECFILE@,%{_datadir}/%{base_name}/%{base_name}.spec,g
' %{SOURCE0} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

install %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_browserpluginsdir}}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/mms.cfg
# http://www.adobe.com/cfusion/knowledgebase/index.cfm?id=16701594
AutoUpdateDisable=1
AutoUpdateInterval=0
EOF
install *.so $RPM_BUILD_ROOT%{_browserpluginsdir}

%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{without license_agreement}
%post
%{_bindir}/%{base_name}.install
%else
%post
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi
%endif

%files
%defattr(644,root,root,755)
%if %{without license_agreement}
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}
%else
%doc *.txt
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mms.cfg
%attr(755,root,root) %{_browserpluginsdir}/*.so
%endif
