#
# Warning: Some old products can cause problems with archetypes - e.g. PortalTransport
#
%define		zope_subname	archetypes
Summary:	Framework designed to facilitate the building of applications for Plone and CMF
Summary(pl.UTF-8):   Środowsko ułatwiające budowanie aplikacji dla Plone i CMF
Name:		Zope-%{zope_subname}
Version:	1.3.7
#%%define		part_name 1-3-7
#%%define		sub_ver rc3
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	http://plone.org/products/archetypes/releases/%{version}-final/archetypes-%{version}-final-bundle.tar.gz
# Source0-md5:	cb169796a54cfe2c063a037604701337
URL:		http://plone.org/products/archetypes/
BuildRequires:	python
BuildRequires:	rpmbuild(macros) >= 1.268
%pyrequires_eq	python-modules
Requires(post,postun):	/usr/sbin/installzopeproduct
Requires:	Zope
Requires:	Zope-CMF
Requires:	Zope-CMFPlone
Requires:	rtf-converter
Obsoletes:	Zope-PortalTransforms
Conflicts:	CMF
Conflicts:	Plone
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Archetypes (formerly known as CMFTypes) is a framework designed to
facilitate the building of applications for Plone and CMF. Its main
purpose is to provide a common method for building content objects,
based on schema definitions.

%description -l pl.UTF-8
Archetypes (poprzednio znany jako CMFTypes) jest środowiskiem
ułatwiającym budowanie aplikacji dla Plone i CMF. Głównym zadaniem
jest dostarczenie podstawowych metod do zbudowania obiektów typu
content opartych na zdefiniowanych schematach.

%prep
%setup -q -c
find . -type d -name debian | xargs rm -rf
find . -type f -name .cvsignore | xargs rm -rf

%build
mkdir docs docs/{Archetypes,MimetypesRegistry,PortalTransforms,generator,validation}
install -d docs/{Archetypes,MimetypesRegistry,PortalTransforms,generator,validation}
mv -f Archetypes/{AUTHORS,ChangeLog,HISTORY.txt,README.txt,TODO.txt} docs/Archetypes
mv -f MimetypesRegistry/{ChangeLog,HISTORY.txt,README} docs/MimetypesRegistry
mv -f PortalTransforms/{ChangeLog,DEPENDS,HISTORY.txt,README,SUGGESTS,TODO} docs/PortalTransforms
rm -rf PortalTransforms/{MANIFEST.in,Makefile}
mv -f generator/{ChangeLog,README,HISTORY.txt} docs/generator
rm -rf {generator,validation}/MANIFEST.in
mv -f validation/{ChangeLog,README,HISTORY.txt} docs/validation

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -af {Archetypes,MimetypesRegistry,PortalTransforms,generator,validation} $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
for p in Archetypes MimetypesRegistry generator validation PortalTransforms; do
	/usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done
%service -q zope restart

%postun
if [ "$1" = "0" ]; then
	for p in Archetypes MimetypesRegistry generator validation PortalTransforms; do
		/usr/sbin/installzopeproduct -d $p
	done
	%service -q zope restart
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%{_datadir}/%{name}
