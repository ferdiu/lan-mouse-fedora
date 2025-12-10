Name:           lan-mouse
Version:        0.10.0
Release:        1%{?dist}
Summary:        Mouse and keyboard sharing software via LAN

License:        GPL-3.0
URL:            https://github.com/feschber/lan-mouse
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Rust dependencies
BuildRequires:  rust-packaging >= 21
BuildRequires:  cargo
BuildRequires:  rust

# GTK/Adwaita dependencies
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

# X11 dependencies for input emulation
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xtst)

# Desktop file utilities
BuildRequires:  desktop-file-utils

# Icon cache update
BuildRequires:  /usr/bin/gtk-update-icon-cache

Requires:       hicolor-icon-theme

# Optional firewalld support
Suggests:       firewalld

%description
Lan Mouse is a cross-platform mouse and keyboard sharing software similar to
universal-control on Apple devices. It allows for using multiple PCs via a
single set of mouse and keyboard. This is also known as a Software KVM switch.

Features:
- Works across Wayland, X11, Windows, and MacOS
- Encrypted network traffic using DTLS
- GTK4/libadwaita frontend
- Command line interface
- Daemon mode support

%prep
%autosetup -n %{name}-%{version}

%build
# Build with release profile
# Skip git operations in build.rs
export CARGO_NET_OFFLINE=true
cargo build -j $(nproc) --release --locked

%install
# Install binary
install -D -m 0755 target/release/lan-mouse %{buildroot}%{_bindir}/lan-mouse

# Install desktop file
desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    de.feschber.LanMouse.desktop

# Install icon
install -D -m 0644 lan-mouse-gtk/resources/de.feschber.LanMouse.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/de.feschber.LanMouse.svg

# Install firewalld service file
install -D -m 0644 firewall/lan-mouse.xml \
    %{buildroot}%{_prefix}/lib/firewalld/services/lan-mouse.xml

# Install systemd user service
install -D -m 0644 service/lan-mouse.service \
    %{buildroot}%{_prefix}/lib/systemd/user/lan-mouse.service

%check
# Desktop file validation
desktop-file-validate %{buildroot}%{_datadir}/applications/de.feschber.LanMouse.desktop

%files
%license LICENSE
%doc README.md config.toml
%{_bindir}/lan-mouse
%{_datadir}/applications/de.feschber.LanMouse.desktop
%{_datadir}/icons/hicolor/scalable/apps/de.feschber.LanMouse.svg
%{_prefix}/lib/firewalld/services/lan-mouse.xml
%{_prefix}/lib/systemd/user/lan-mouse.service

%changelog
* Wed Dec 10 2025 Federico Manzella <ferdiu.manzella@gmail.com> - 0.10.0-1
- Initial RPM package for Fedora
- Version 0.10.0 release
