#
# Warning: Some old products can cause problems with archetypes - e.g. PortalTransport
#
%define		zope_subname	archetypes
Summary:	Framework designed to facilitate the building of applications for Plone and CMF
Summary(pl):	¦rodowsko u³atwiaj±ce budowanie aplikacji dla Plone i CMF
Name:		Zope-%{zope_subname}
Version:	1.3.1
#%%define		sub_ver rc3
Release:	2
License:	GPL
Group:		Development/Tools
Source0:	http://dl.sourceforge.net/archetypes/Archetypes-%{version}-final-Bundle.tar.gz
# Source0-md5:	99094266adf7a845eccf95aa46e28863
URL:		http://dreamcatcher.homeunix.org/
BuildRequires:	python
%pyrequires_eq	python-modules
Requires:	Zope
Requires:	Zope-CMFPlone
Requires:	Zope-CMF
Requires:	rtf-converter
Requires(post,postun):	/usr/sbin/installzopeproduct
Obsoletes:	Zope-PortalTransforms
Conflicts:	CMF
Conflicts:	Plone
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Archetypes (formerly known as CMFTypes) is a framework designed 
to facilitate the building of applications for Plone and CMF. 
Its main purpose is to provide a common method for building 
content objects, based on schema definitions. 

%description -l pl
Archetypes (poprzednio znany jako CMFTypes) jest ¶rodowiskiem
u³atwiaj±cym budowanie aplikacji dla Plone i CMF.
G³ównym zadaniem jest dostarczenie podstawowych metod 
do zbudowania obiektów typu content opartych na zdefiniowanych
schematach. 

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
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%postun
if [ "$1" = "0" ]; then
	for p in Archetypes MimetypesRegistry generator validation PortalTransforms; do
		/usr/sbin/installzopeproduct -d $p
	done
fi
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%files
%defattr(644,root,root,755)
%doc docs/* 
%{_datadir}/%{name}
