# 
# TODO
# - check this version on Zope, Plone and CMF
#
%define		zope_subname	archetypes
Summary:	Framework designed to facilitate the building of applications for Plone and CMF. 
Summary(pl):	¦rodowsko u³atwiaj±ce budowanie aplikacji dla Plone i CMF.
Name:		Zope-%{zope_subname}
Version:	1.2.0
Release:	2
License:	GPL
Group:		Development/Tools
Source0:	http://dl.sourceforge.net/%{zope_subname}/%{zope_subname}-%{version}.tgz
# Source0-md5:	b25fdf747a286488b17e512205f4f1ac
URL:		http://dreamcatcher.homeunix.org/
%pyrequires_eq	python-modules
Requires:	Zope-CMF
Requires:	Zope-CMFPlone
Requires:	Zope
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
Archetypes (poprzednio znany jako CMFTypes) jest ¶rodowskiem
u³atwiaj±cym budowanie aplikacji dla Plone i CMF.
G³ównym zadaniem jest dostarczenie podstawowych metod 
do zbudowania obiektów typu content opartych na zdefiniowanych
schematach. 

%prep
%setup -q -c
rm -f %{zope_subname}-%{version}/ArchGenXML/.cvsignore
find . -type d -name debian | xargs rm -rf

%build
install -d docs/{ArchExample,ArchGenXML,Archetypes,generator,validation}
cd %{zope_subname}-%{version}
mv -f ArchExample/ChangeLog ../docs/ArchExample
mv -f ArchGenXML/README ../docs/ArchGenXML
mv -f Archetypes/{docs/*,AUTHORS,ChangeLog,README.txt,TODO.txt} ../docs/Archetypes
rm -rf Archetypes/docs
mv -f generator/{ChangeLog,README} ../docs/generator
mv -f validation/{ChangeLog,README} ../docs/validation

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{py_sitedir}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -af %{zope_subname}-%{version}/{generator,validation} $RPM_BUILD_ROOT%{py_sitedir}
cp -af %{zope_subname}-%{version}/{ArchExample,ArchGenXML,Archetypes} $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}

rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
for p in ArchExample ArchGenXML Archetypes ; do
    /usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%postun
if [ "$1" = "0" ]; then
    for p in ArchExample ArchGenXML Archetypes ; do
        /usr/sbin/installzopeproduct -d $p
    done
fi
if [ -f /var/lock/subsys/zope ]; then
            /etc/rc.d/init.d/zope restart >&2
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%{_datadir}/%{name}/ArchExample
%{_datadir}/%{name}/ArchGenXML
%{_datadir}/%{name}/Archetypes
%{py_sitedir}/generator
%{py_sitedir}/validation
