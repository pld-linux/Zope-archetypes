%include	/usr/lib/rpm/macros.python

%define		zope_subname	archetypes

Summary:	Archetypes - a framework for developing new content types in Plone
Summary(pl):	Archetypes - nowe ¶rodowisko pracy dla twórców serwisów Plone
Name:		Zope-%{zope_subname}
Version:	1.0.1
Release:	1
License:	GNU
Group:		Development/Tools
Source0:	http://dl.sourceforge.net/%{zope_subname}/%{zope_subname}-%{version}.tgz
# Source0-md5:	53f3ccf5a88ce3a91b50e8a82165c2de
URL:		http://dreamcatcher.homeunix.org/
%pyrequires_eq	python-modules
Requires:	CMF
Requires:	Plone
Requires:	Zope
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	product_dir	/usr/lib/zope/Products

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
%setup -q -c %{zope_subname}-%{version}

%build
mkdir docs docs/ArchExample docs/ArchGenXML docs/Archetypes docs/generator docs/validation
cd %{zope_subname}-%{version}
mv -f *.pdf ../docs/
mv -f ArchExample/ChangeLog ../docs/ArchExample
mv -f ArchGenXML/README ../docs/ArchGenXML
mv -f Archetypes/{/docs/*,AUTHORS,ChangeLog,README.txt,TODO.txt} ../docs/Archetypes
rm -rf Archetypes/docs
mv -f generator/{ChangeLog,MANIFEST.in,README} ../docs/generator
mv -f validation/{ChangeLog,MANIFEST.in,README} ../docs/validation

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{product_dir}

cd %{zope_subname}-%{version}
cp -af * $RPM_BUILD_ROOT%{product_dir}

%py_comp $RPM_BUILD_ROOT%{product_dir}
%py_ocomp $RPM_BUILD_ROOT%{product_dir}

# find $RPM_BUILD_ROOT -type f -name "*.py" -exec rm -rf {} \;;
rm -rf $RPM_BUILD_ROOT%{product_dir}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%postun
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%{product_dir}/ArchExample
%{product_dir}/ArchGenXML
%{product_dir}/Archetypes
%{product_dir}/generator
%{product_dir}/validation
