%global real_name hachoir

Name:           python-%{real_name}
Version:        3.3.0
Release:        1%{?dist}
Summary:        Python library to view and edit a binary stream field by field
License:        GPL-2.0-only
BuildArch:      noarch

URL:            https://github.com/vstinner/%{real_name}
Source0:        %{url}/archive/%{version}/%{real_name}-%{version}.tar.gz

# urwid 2.1 moved the display modules under urwid.display and 3.0 dropped the
# old top-level alias; submitted upstream is not possible as the project is in
# maintenance mode, so carry it here.
Patch0:         0001-Support-urwid-2.1.patch

BuildRequires:  python3-devel
# For %%check: the optional interfaces are only importable with these present.
BuildRequires:  python3-urwid
BuildRequires:  python3-wxpython4


%global _description %{expand:
Hachoir is a Python library used to represent a binary file as a tree of Python
objects. Each object has a type, a value, an address, a description and a size
in bits. Hachoir can parse a large number of file formats (archives, audio and
video containers, images, executables, filesystems) and is able to browse and
edit them field by field.}

%description %_description

%package -n     python3-%{real_name}
Summary:        %{summary}

%description -n python3-%{real_name} %_description

%package -n     python3-%{real_name}-urwid
Summary:        Text user interface to explore binary files with hachoir
Requires:       python3-%{real_name} = %{version}-%{release}
Requires:       python3-urwid

%description -n python3-%{real_name}-urwid
The hachoir-urwid command, an interactive text user interface to explore a
binary file field by field.

%package -n     python3-%{real_name}-wx
Summary:        Graphical user interface to explore binary files with hachoir
Requires:       python3-%{real_name} = %{version}-%{release}
Requires:       python3-wxpython4

%description -n python3-%{real_name}-wx
The hachoir-wx command, a wxPython graphical user interface to explore a binary
file field by field.

%prep
%autosetup -n %{real_name}-%{version} -p1

# These two are imported as modules, they are not run directly; the commands are
# generated from the entry points instead.
sed -i '1{/^#!/d}' %{real_name}/subfile/__main__.py %{real_name}/wx/main.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{real_name}

%check
# Three leaf modules cannot be imported on a current system and are left as
# upstream ships them: core.profiler needs hotshot (gone from Python 3, and only
# imported on demand by the --profiler options), metadata.qt needs PyQt4 and
# metadata.gtk needs the GTK 3 typelib. None of them backs an installed command.
%pyproject_check_import -e %{real_name}.core.profiler -e %{real_name}.metadata.gtk -e %{real_name}.metadata.qt.main

%files -n python3-%{real_name} -f %{pyproject_files}
%doc README.rst doc/*.rst
%license COPYING
%{_bindir}/%{real_name}-grep
%{_bindir}/%{real_name}-metadata
%{_bindir}/%{real_name}-strip
%exclude %{python3_sitelib}/%{real_name}/urwid.py
%exclude %{python3_sitelib}/%{real_name}/__pycache__/urwid.*
%exclude %{python3_sitelib}/%{real_name}/wx/

%files -n python3-%{real_name}-urwid
%{_bindir}/%{real_name}-urwid
%{python3_sitelib}/%{real_name}/urwid.py
%{python3_sitelib}/%{real_name}/__pycache__/urwid.*

%files -n python3-%{real_name}-wx
%{_bindir}/%{real_name}-wx
%{python3_sitelib}/%{real_name}/wx/

%changelog
* Thu Sep 10 2026 Simone Caronni <negativo17@gmail.com> - 3.3.0-1
- First build.
