#
# Warning: problem with start Zope
#
%define		zope_subname	archetypes
Summary:	Framework designed to facilitate the building of applications for Plone and CMF. 
Summary(pl):	�rodowsko u�atwiaj�ce budowanie aplikacji dla Plone i CMF.
Name:		Zope-%{zope_subname}
Version:	1.3.0
%define		sub_ver rc3
Release:	0.%{sub_ver}.2
License:	GPL
Group:		Development/Tools
Source0:	http://dl.sourceforge.net/%{zope_subname}/Archetypes-%{version}-%{sub_ver}.tar.gz
# Source0-md5:	f523268f6605d6a7bd2d652db091717a
URL:		http://dreamcatcher.homeunix.org/
%pyrequires_eq	python-modules
Requires:	Zope
Requires:	Zope-CMFPlone
Requires:	Zope-CMF
Requires(post,postun):  /usr/sbin/installzopeproduct
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	CMF
Conflicts:	Plone
Obsoletes:	Zope-PortalTransforms

%description
Archetypes (formerly known as CMFTypes) is a framework designed 
to facilitate the building of applications for Plone and CMF. 
Its main purpose is to provide a common method for building 
content objects, based on schema definitions. 

%description -l pl
Archetypes (poprzednio znany jako CMFTypes) jest �rodowskiem
u�atwiaj�cym budowanie aplikacji dla Plone i CMF.
G��wnym zadaniem jest dostarczenie podstawowych metod 
do zbudowania obiekt�w typu content opartych na zdefiniowanych
schematach. 

%prep
%setup -q -c
find . -type d -name debian | xargs rm -rf
find . -type f -name .cvsignore | xargs rm -rf

%build
mkdir docs docs/{Archetypes,MimetypesRegistry,PortalTransforms,generator,validation}
install -d docs/{Archetypes,MimetypesRegistry,generator,validation}
mv -f Archetypes-%{version}-%{sub_ver}/Archetypes/{AUTHORS,ChangeLog,HISTORY.txt,README.txt,DEPENDS,TODO.txt} docs/Archetypes
rm -rf Archetypes-%{version}-%{sub_ver}/Archetypes/LICENSE.*
mv -f Archetypes-%{version}-%{sub_ver}/MimetypesRegistry/{ChangeLog,HISTORY.txt,README} docs/MimetypesRegistry
rm -rf Archetypes-%{version}-%{sub_ver}/MimetypesRegistry/LICENSE.txt
mv -f Archetypes-%{version}-%{sub_ver}/PortalTransforms/{ChangeLog,DEPENDS,HISTORY.txt,README,SUGGESTS,TODO} docs/PortalTransforms
rm -rf Archetypes-%{version}-%{sub_ver}/PortalTransforms/{LICENSE.txt,MANIFEST.in,Makefile}
mv -f Archetypes-%{version}-%{sub_ver}/generator/{ChangeLog,README,HISTORY.txt} docs/generator
rm -rf Archetypes-%{version}-%{sub_ver}/{generator,validation}/MANIFEST.in
mv -f Archetypes-%{version}-%{sub_ver}/validation/{ChangeLog,README,HISTORY.txt} docs/validation

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -af Archetypes-%{version}-%{sub_ver}/{Archetypes,MimetypesRegistry,PortalTransforms,generator,validation} $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

# rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
for p in Archetypes MimetypesRegistry PortalTransforms generator validation; do
    /usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%postun
if [ "$1" = "0" ]; then
    for p in Archetypes MimetypesRegistry PortalTransforms generator validation; do
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
