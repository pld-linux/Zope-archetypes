# 
# TODO
# - check this version on stable branch - on Zope 2.7.0b3 and Plone 2.0b3 Zope starting but 
#   connection refused (on WWW)!
#
%define		zope_subname	archetypes
Summary:	A framework for developing new content types in Plone
Summary(pl):	Nowe ¶rodowisko pracy dla twórców serwisów Plone
Name:		Zope-%{zope_subname}
Version:	1.2.0
Release:	1
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
Archetypes is a framework for developing new content types in
Plone. The power of Archetypes is, first, in automatically generating
forms; second, in providing a library of stock field types, form
widgets, and field validators; third, in easily integrating custom
fields, widgets, and validators; and fourth, in automating
transformations of rich content.

%description -l pl
Archetypes jest nowym ¶rodowiskiem pracy dla twórców serwisów
Plone. Si³± Archetypes s± automatycznie generowane formularze,
zarz±dzalne biblioteki pól typów, kontrolek i korektorów pól, a tak¿e
³atwa integracja zaawansowanych mo¿liwo¶ci z w/w typami. Posiada
równie¿ bogat± automatykê.

%prep
%setup -q -c
rm -f %{zope_subname}-%{version}/ArchGenXML/.cvsignore

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
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

# should {Archetypes,validation}/tests and */version.txt be installed or not?
cp -af %{zope_subname}-%{version}/{ArchExample,ArchGenXML,Archetypes,generator,validation} $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

# find $RPM_BUILD_ROOT -type f -name "*.py" -exec rm: -rf {} \;;
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
for p in ArchExample ArchGenXML Archetypes generator validation ; do
    /usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%postun
if [ "$1" = "0" ]; then
    for p in ArchExample ArchGenXML Archetypes generator validation ; do
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
