#
# Conditional build:
%bcond_without	systemd	# systemd inhibit service

Summary:	MATE power management service
Summary(pl.UTF-8):	Usługa zarządzania energią dla MATE
Name:		mate-power-manager
Version:	1.18.0
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.18/%{name}-%{version}.tar.xz
# Source0-md5:	0752b149f3036fb0469afa57edf3d3a2
URL:		http://wiki.mate-desktop.org/mate-power-manager
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.9
BuildRequires:	cairo-devel >= 1.0.0
BuildRequires:	dbus-devel >= 1.0
BuildRequires:	dbus-glib-devel >= 0.70
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
BuildRequires:	gettext-tools >= 0.10.40
BuildRequires:	glib2-devel >= 1:2.36.0
BuildRequires:	gtk+3-devel >= 3.14
BuildRequires:	intltool >= 0.50.1
BuildRequires:	libcanberra-gtk3-devel >= 0.10
BuildRequires:	libgnome-keyring-devel >= 3.0.0
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libtool >= 2:2
BuildRequires:	mate-common
BuildRequires:	mate-panel-devel >= 1.17.0
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	rpmbuild(find_lang) >= 1.36
%{?with_systemd:BuildRequires:	systemd-devel >= 1:195}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXrandr-devel >= 1.3.0
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-proto-xproto-devel >= 7.0.15
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	cairo >= 1.0.0
Requires:	dbus >= 1.0
Requires:	dbus-glib >= 0.70
Requires:	glib2 >= 1:2.36.0
Requires:	gtk+3 >= 3.14
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	libcanberra-gtk3 >= 0.10
Requires:	libgnome-keyring >= 3.0.0
Requires:	libnotify >= 0.7.0
Requires:	mate-panel >= 1.17.0
Requires:	xorg-lib-libXrandr >= 1.3.0
Suggests:	udisks
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/mate-panel

%description
MATE Power Manager uses the information and facilities provided by
UPower displaying icons and handling user callbacks in an interactive
MATE session.

%description -l pl.UTF-8
MATE Power Manager wykorzystuje informacje i funkcje udostępniane
przez UPower do wyświetlania ikon i obsługi reakcji użytkownika w
interaktywnej sesji MATE.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-applets \
	--disable-silent-rules \
	--disable-static \
	%{!?with_systemd:--without-systemdinhibit}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{ku_IQ,pms}

%find_lang %{name} --with-mate

desktop-file-install \
	--delete-original \
	--remove-category=MATE \
	--add-category=X-Mate \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/*.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%update_icon_cache hicolor
%glib_compile_schemas

%files  -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
/etc/xdg/autostart/mate-power-manager.desktop
%attr(755,root,root) %{_bindir}/mate-power-manager
%attr(755,root,root) %{_bindir}/mate-power-preferences
%attr(755,root,root) %{_bindir}/mate-power-statistics
%attr(755,root,root) %{_sbindir}/mate-power-backlight-helper
%attr(755,root,root) %{_libexecdir}/mate-brightness-applet
%attr(755,root,root) %{_libexecdir}/mate-inhibit-applet
%{_mandir}/man1/mate-power-backlight-helper.1*
%{_mandir}/man1/mate-power-manager.1*
%{_mandir}/man1/mate-power-preferences.1*
%{_mandir}/man1/mate-power-statistics.1*
%{_datadir}/%{name}
%{_datadir}/mate-panel/applets/org.mate.BrightnessApplet.mate-panel-applet
%{_datadir}/mate-panel/applets/org.mate.InhibitApplet.mate-panel-applet
%{_datadir}/dbus-1/services/org.mate.PowerManager.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.BrightnessAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.InhibitAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.power-manager.gschema.xml
%{_datadir}/polkit-1/actions/org.mate.power.policy
%{_desktopdir}/mate-power-preferences.desktop
%{_desktopdir}/mate-power-statistics.desktop
%{_iconsdir}/hicolor/*/apps/mate-brightness-applet.*
%{_iconsdir}/hicolor/*/apps/mate-inhibit-applet.*
%{_iconsdir}/hicolor/*/apps/mate-power-manager.*
%{_iconsdir}/hicolor/*/apps/mate-power-statistics.*
