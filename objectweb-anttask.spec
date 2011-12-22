# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define _with_bootstrap 0

%define with_bootstrap %{!?_with_bootstrap:0}%{?_with_bootstrap:1}
%define without_bootstrap %{?_with_bootstrap:0}%{!?_with_bootstrap:1}

%define section         free

Summary:        ObjectWeb Ant task
Name:           objectweb-anttask
Version:        1.3.2
Release:        3.6%{?dist}
Epoch:          0
Group:          Development/Tools
License:        LGPLv2+
URL:            http://forge.objectweb.org/projects/monolog/
BuildArch:      noarch
Source0:        http://download.forge.objectweb.org/monolog/ow_util_ant_tasks_1.3.2.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  java-devel
BuildRequires:  ant >= 0:1.6
BuildRequires:  jpackage-utils >= 0:1.6

%if %{without_bootstrap}
BuildRequires:  asm2
Requires:       asm2
%endif

Requires(post):   jpackage-utils 
Requires(postun): jpackage-utils
Provides:         owanttask = %{epoch}:%{version}-%{release}

%description
ObjectWeb Ant task

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Documentation

%description    javadoc
Javadoc for %{name}.

%prep
%setup -c -q -n %{name}

# extract jars iff in bootstrap mode
%if %{without_bootstrap}
find . -name "*.class" -exec rm {} \;
find . -name "*.jar" -exec rm {} \;
%endif

%build
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java
export CLASSPATH=$(build-classpath asm2/asm2)
ant -Dbuild.compiler=modern -Dbuild.sysclasspath=first jar jdoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}

install -m 644 output/lib/ow_util_ant_tasks.jar\
 $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
pushd $RPM_BUILD_ROOT%{_javadir}
  ln -sf %{name}-%{version}.jar %{name}.jar
popd

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr output/jdoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
(cd $RPM_BUILD_ROOT%{_javadocdir} && ln -sf %{name}-%{version} %{name})

%clean
rm -rf $RPM_BUILD_ROOT

#%post javadoc
#rm -f %{_javadocdir}/%{name}
#ln -s %{name}-%{version} %{_javadocdir}/%{name}

#%postun javadoc
#if [ $1 -eq 0 ]; then
#  rm -f %{_javadocdir}/%{name}
#fi

%files
%defattr(0644,root,root,0755)
%doc doc/* 
%doc output/jdoc/*
%{_javadir}/*

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}
%doc %{_javadocdir}/%{name}-%{version}
%ghost %dir %{_javadocdir}/%{name}

%changelog
* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0:1.3.2-3.6
- Fix Group tags
- Fix Source0 URL.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:1.3.2-3.5
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-3.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-2.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.3.2-1.4
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0:1.3.2-1jpp.3
- fix license tag

* Wed Aug 29 2007 Deepak Bhole <dbhole@redhat.com> 0:1.3.2-1jpp.2
- Remove distribution tag

* Mon Feb 12 2007 Tania Bento <tbento@redhat.com> 0:1.3.2-1jpp.1
- Changed %%BuildRoot tag.
- Bootstrap Buildling.
- Should not touch buildroot in %%prep.
- Removed %%Vendor tag.
- Removed %%Distribution tag.
- Fixed %%Release tag.
- Fixed %%Sourcei0 tag.
- Added %%doc to %%files section.
- Edited %%doc in %%files javadoc section.

* Thu Jul 20 2006 Ralph Apel <r.apel at r-apel.de> 0:1.3.2-1jpp
- First JPP-1.7 release
- Upgrade to 1.3.2, now requires asm2
- Add javadoc subpackage

* Mon Sep 20 2004 Ralph Apel <r.apel at r-apel.de> 0:1.2-1jpp
- First JPackage release


