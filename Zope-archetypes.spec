%define		zope_subname	archetypes
Summary:	Framework designed to facilitate the building of applications for Plone and CMF. 
Summary(pl):	Środowsko ułatwiające budowanie aplikacji dla Plone i CMF.
Name:		Zope-%{zope_subname}
Version:	1.2.5
%define		sub_ver rc4
Release:	0.%{sub_ver}.1
License:	GPL
Group:		Development/Tools
Source0:	http://dl.sourceforge.net/%{zope_subname}/%{zope_subname}-%{version}-%{sub_ver}.tgz
# Source0-md5:	15aa7eb4ef06f8f06852a39e86c4f3e0
URL:		http://dreamcatcher.homeunix.org/
%pyrequires_eq	python-modules
Requires:	Zope
Requires:	Zope-CMFPlone
Requires:	Zope-CMF
Requires:	Zope-PortalTransforms
Requires(post,postun):  /usr/sbin/installzopeproduct
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	CMF
Conflicts:	Plone

%description
Archetypes (formerly known as CMFTypes) is a framework designed 
to facilitate the building of applications for Plone and CMF. 
Its main purpose is to provide a common method for building 
content objects, based on schema definitions. 

%description -l pl
Archetypes (poprzednio znany jako CMFTypes) jest środowskiem
ułatwiającym budowanie aplikacji dla Plone i CMF.
Głównym zadaniem jest dostarczenie podstawowych metod 
do zbudowania obiektów typu content opartych na zdefiniowanych
schematach. 

%prep
%setup -q -c
find . -type d -name debian | xargs rm -rf

%build
install -d docs/{ArchExample,ArchGenXML,Archetypes,generator,validation}
mv -f %{zope_subname}-%{version}-%{sub_ver}/ArchExample/ChangeLog docs/ArchExample
mv -f %{zope_subname}-%{version}-%{sub_ver}/ArchGenXML/{README,CREDITS} docs/ArchGenXML
mv -f %{zope_subname}-%{version}-%{sub_ver}/Archetypes/{AUTHORS,ChangeLog,README.txt,TODO.txt,DEPENDS} docs/Archetypes
rm -rf %{zope_subname}-%{version}-%{sub_ver}/Archetypes/LICENSE.*
mv -f %{zope_subname}-%{version}-%{sub_ver}/generator/{ChangeLog,README} docs/generator
rm -rf %{zope_subname}-%{version}-%{sub_ver}/{generator,validation}/MANIFEST.in
mv -f %{zope_subname}-%{version}-%{sub_ver}/validation/{ChangeLog,README} docs/validation

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -af %{zope_subname}-%{version}-%{sub_ver}/{ArchExample,ArchGenXML,Archetypes,generator,validation} $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

# rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
for p in ArchExample ArchGenXML Archetypes generator validation; do
    /usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%postun
if [ "$1" = "0" ]; then
    for p in ArchExample ArchGenXML Archetypes generator validation; do
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
