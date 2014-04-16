#
# Conditional build:
%bcond_with	gtk3	# use GTK+ 3.x instead of 2.x
%bcond_without	systemd	# systemd inhibit service

Summary:	MATE power management service
Summary(pl.UTF-8):	Usługa zarządzania energią dla MATE
Name:		mate-power-manager
Version:	1.8.0
Release:	2
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	09688f0422adce20de79f17d2f7a07b0
Patch0:		uidir.patch
Patch1:		mate-power-manager_upower.patch
Patch2:		mate-power-manager_upower-remove-recall.patch
Patch3:		mate-power-manager_upower-use-g_signal-notify.patch
Patch4:		mate-power-manager_upower-update-for-libupower-glib-API-changes.patch
Patch5:		mate-power-manager_fix-use-g_signal-notify.patch
URL:		http://wiki.mate-desktop.org/mate-power-manager
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.9
BuildRequires:	cairo-devel >= 1.0.0
BuildRequires:	dbus-devel >= 1.0
BuildRequires:	dbus-glib-devel >= 0.70
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
BuildRequires:	gettext-devel >= 0.10.40
BuildRequires:	glib2-devel >= 1:2.26.0
%{!?with_gtk2:BuildRequires:	gtk+2-devel >= 2:2.17.7}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libcanberra-gtk-devel >= 0.10
BuildRequires:	libgnome-keyring-devel >= 3.0.0
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libtool >= 2:2
%{!?with_gtk3:BuildRequires:	libunique-devel >= 0.9.4}
%{?with_gtk3:BuildRequires:	libunique3-devel >= 3.0}
BuildRequires:	mate-common
BuildRequires:	mate-panel-devel >= 1.5.0
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	rpmbuild(find_lang) >= 1.36
%{?with_systemd:BuildRequires:	systemd-devel >= 1:195}
BuildRequires:	tar >= 1:1.22
BuildRequires:	upower-devel >= 0.9.1
BuildRequires:	xorg-lib-libXrandr-devel >= 1.3
BuildRequires:	xorg-proto-xproto-devel >= 7.0.15
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	cairo >= 1.0.0
Requires:	dbus >= 1.0
Requires:	dbus-glib >= 0.70
Requires:	glib2 >= 1:2.26.0
%{!?with_gtk2:Requires:	gtk+2 >= 2:2.17.7}
%{?with_gtk3:Requires:	gtk+3 >= 3.0.0}
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	libcanberra-gtk >= 0.10
Requires:	libgnome-keyring >= 0.6.0
Requires:	libnotify >= 0.7.0
%{!?with_gtk3:Requires:	libunique >= 0.9.4}
%{?with_gtk3:Requires:	libunique3 >= 3.0}
Requires:	mate-panel >= 1.5.0
Requires:	upower >= 0.9.1
Requires:	xorg-lib-libXrandr >= 1.3
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-applets \
	--disable-scrollkeeper \
	--disable-silent-rules \
	--disable-static \
	%{?with_gtk3:--with-gtk=3.0} \
	%{!?with_systemd:--without-systemdinhibit}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

# mate < 1.5 did not exist in pld, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/mate-power-manager.convert
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/cmn

%find_lang %{name} --with-mate --with-omf

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
%attr(755,root,root) %{_bindir}/mate-power-bugreport.sh
%attr(755,root,root) %{_bindir}/mate-power-manager
%attr(755,root,root) %{_bindir}/mate-power-preferences
%attr(755,root,root) %{_bindir}/mate-power-statistics
%attr(755,root,root) %{_sbindir}/mate-power-backlight-helper
%attr(755,root,root) %{_libexecdir}/mate-brightness-applet
%attr(755,root,root) %{_libexecdir}/mate-inhibit-applet
%{_mandir}/man1/mate-power-manager.1*
%{_mandir}/man1/mate-power-preferences.1*
%{_mandir}/man1/mate-power-statistics.1*
%{_datadir}/%{name}
%{_datadir}/mate-panel/applets/org.mate.BrightnessApplet.mate-panel-applet
%{_datadir}/mate-panel/applets/org.mate.InhibitApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/brightness-applet-menu.xml
%{_datadir}/mate-panel/ui/inhibit-applet-menu.xml
%{_datadir}/dbus-1/services/mate-power-manager.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.BrightnessAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.InhibitAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.power-manager.gschema.xml
%{_datadir}/polkit-1/actions/org.mate.power.policy
%{_desktopdir}/mate-power-preferences.desktop
%{_desktopdir}/mate-power-statistics.desktop
%{_iconsdir}/hicolor/*/apps/mate-*.*
