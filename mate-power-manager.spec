#
# Conditional build:
%bcond_without	systemd		# without systemd inhibit

Summary:	MATE power management service
Name:		mate-power-manager
Version:	1.6.1
Release:	2
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	de091940b4696108daea32ef64ec9926
Patch1:		use-gnome-keyring.patch
Patch4:		uidir.patch
URL:		http://wiki.mate-desktop.org/mate-power-manager
BuildRequires:	cairo-devel >= 1.0.0
BuildRequires:	dbus-glib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
BuildRequires:	glib2-devel
BuildRequires:	gtk+2-devel >= 2:2.17.7
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libcanberra-devel
BuildRequires:	libcanberra-gtk-devel
BuildRequires:	libgnome-keyring-devel >= 0.6.0
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libunique-devel
BuildRequires:	mate-common
BuildRequires:	mate-doc-utils
BuildRequires:	mate-panel-devel
BuildRequires:	popt-devel
BuildRequires:	rpmbuild(find_lang) >= 1.36
%{?with_systemd:BuildRequires:	systemd-devel >= 1:195}
BuildRequires:	tar >= 1:1.22
BuildRequires:	upower-devel
BuildRequires:	xz
Requires:	glib2 >= 1:2.26.0
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	mate-panel >= 1.5.0
Requires:	upower
Suggests:	udisks
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/mate-panel

%description
MATE Power Manager uses the information and facilities provided by
UPower displaying icons and handling user callbacks in an interactive
MATE session.

%prep
%setup -q
%patch1 -p1
%patch4 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	--disable-scrollkeeper \
	%{!?with_systemd:--without-systemdinhibit} \
	--enable-applets

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

# mate < 1.5 did not exist in pld, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/mate-power-manager.convert

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
%doc AUTHORS README
/etc/xdg/autostart/mate-power-manager.desktop
%attr(755,root,root) %{_bindir}/mate-power-bugreport.sh
%attr(755,root,root) %{_bindir}/mate-power-manager
%attr(755,root,root) %{_bindir}/mate-power-preferences
%attr(755,root,root) %{_bindir}/mate-power-statistics
%attr(755,root,root) %{_sbindir}/mate-power-backlight-helper
%attr(755,root,root) %{_libdir}/mate-panel/mate-brightness-applet
%attr(755,root,root) %{_libdir}/mate-panel/mate-inhibit-applet
%{_mandir}/man1/mate-power-manager.1*
%{_mandir}/man1/mate-power-preferences.1*
%{_mandir}/man1/mate-power-statistics.1*
%{_datadir}/%{name}
%{_desktopdir}/mate-power-preferences.desktop
%{_desktopdir}/mate-power-statistics.desktop
%{_iconsdir}/hicolor/*/apps/mate-*.*
%{_datadir}/mate-panel/applets/org.mate.BrightnessApplet.mate-panel-applet
%{_datadir}/mate-panel/applets/org.mate.InhibitApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/brightness-applet-menu.xml
%{_datadir}/mate-panel/ui/inhibit-applet-menu.xml
%{_datadir}/dbus-1/services/mate-power-manager.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.BrightnessAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.InhibitAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.power-manager.gschema.xml
%{_datadir}/polkit-1/actions/org.mate.power.policy
