%{?_javapackages_macros:%_javapackages_macros}
%global ver  1.50
%global archivever  jdk15on-%(echo %{ver}|sed 's|\\\.||')

Summary:          S/MIME and CMS libraries for Bouncy Castle
Name:             bouncycastle-mail
Version:          %{ver}
Group:		  System/Libraries
Release:          5%{?dist}
License:          MIT
URL:              https://www.bouncycastle.org/
Source0:          http://www.bouncycastle.org/download/bcmail-%{archivever}.tar.gz
Source1:          http://repo2.maven.org/maven2/org/bouncycastle/bcmail-jdk15on/%{version}/bcmail-jdk15on-%{version}.pom

BuildArch:        noarch
BuildRequires:    bouncycastle = %{version}
BuildRequires:    bouncycastle-pkix = %{version}
BuildRequires:    java-devel >= 1.7
BuildRequires:    javamail
BuildRequires:    javapackages-tools
BuildRequires:    junit
Requires:         bouncycastle = %{version}
Requires:         bouncycastle-pkix = %{version}
Requires:         java-headless >= 1.7
Requires:         javamail
Requires:         javapackages-tools
Provides:         bcmail = %{version}-%{release}

%description
Bouncy Castle consists of a lightweight cryptography API and is a provider 
for the Java Cryptography Extension and the Java Cryptography Architecture.
This library package offers additional classes, in particuar 
generators/processors for S/MIME and CMS, for Bouncy Castle.

%package javadoc
Summary:        Javadoc for %{name}
Requires:       %{name} = %{version}-%{release}

%description javadoc
API documentation for the %{name} package.

%prep
%setup -q -n bcmail-%{archivever}
mkdir src
unzip -qq src.zip -d src/

find . -type f -name "*.class" -delete
find . -type f -name "*.jar" -delete

# too many "IOException: Stream closed" failures
rm -f src/org/bouncycastle/mail/smime/test/AllTests.java

# package org.bouncycastle.cms.test does not exist
rm -f src/org/bouncycastle/mail/smime/test/NewSMIMEEnvelopedTest.java
rm -f src/org/bouncycastle/mail/smime/test/NewSMIMESignedTest.java
rm -f src/org/bouncycastle/mail/smime/test/SMIMECompressedTest.java
rm -f src/org/bouncycastle/mail/smime/test/SMIMEMiscTest.java
rm -f src/org/bouncycastle/mail/smime/test/SignedMailValidatorTest.java

cp %{SOURCE1} pom.xml

%build
pushd src
  export CLASSPATH=$(build-classpath junit bcprov bcpkix javamail)
  %javac -g -source 1.6 -target 1.6 -encoding UTF-8 $(find . -type f -name "*.java")
  jarfile="../bcmail.jar"
  # Exclude all */test/* , cf. upstream
  files="$(find . -type f \( -name '*.class' -o -name '*.properties' \) -not -path '*/test/*')"
  test ! -d classes && mf="" \
    || mf="`find classes/ -type f -name "*.mf" 2>/dev/null`"
  test -n "$mf" && %jar cvfm $jarfile $mf $files \
    || %jar cvf $jarfile $files
popd

%install
# install bouncy castle mail
install -dm 755 $RPM_BUILD_ROOT%{_javadir}
install -pm 644 bcmail.jar \
  $RPM_BUILD_ROOT%{_javadir}/bcmail.jar

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# maven pom
install -dm 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-bcmail.pom
%add_maven_depmap -a "org.bouncycastle:bcmail-jdk16" JPP-bcmail.pom bcmail.jar

%check
pushd src
  export CLASSPATH=$PWD:$(build-classpath junit javamail bcprov bcpkix)
  for test in $(find . -name AllTests.class) ; do
    test=${test#./} ; test=${test%.class} ; test=${test//\//.}
    %java org.junit.runner.JUnitCore $test
  done
popd

%files -f .mfiles
%doc *.html
%{_javadir}/bcmail.jar
%{_mavenpomdir}/JPP-bcmail.pom

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Tue Jun 10 2014 Alexander Kurtakov <akurtako@redhat.com> 1.50-5
- Fix FTBFS.
- Drop gcj support.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 gil cattaneo <puntogil@libero.it> 1.50-3
- add bcpkix suppport

* Tue Feb 25 2014 Michal Srb <msrb@redhat.com> - 1.50-2
- Remove unavailable dep from pom.xml

* Mon Feb 24 2014 Michal Srb <msrb@redhat.com> - 1.50-1
- Update to upstream version 1.50
- Switch to java-headless (Resolves: rhbz#1067986)
- Enable (some) tests

* Tue Oct 22 2013 gil cattaneo <puntogil@libero.it> 1.46-11
- remove versioned Jars

* Mon Aug 12 2013 gil cattaneo <puntogil@libero.it> 1.46-10
- rebuilt rhbz#995893

* Mon Aug 05 2013 gil cattaneo <puntogil@libero.it> 1.46-9
- rebuilt rhbz#992027

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 08 2012 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.46-5
- use original sources from here on out

* Sat Feb 18 2012 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.46-4
- Build with -source 1.6 -target 1.6

* Thu Jan 12 2012 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.46-3
- Update javac target version to 1.7 to build with new java

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 01 2011 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.46-1
- Import Bouncy Castle 1.46.
- Drop gcj.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 11 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.45-1
- Import Bouncy Castle 1.45.

* Sat Nov 14 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.44-1
- Import Bouncy Castle 1.44.

* Thu Sep 17 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.43-5
- Similar fixes proposed in RHBZ#521475, namely:
- Include missing properties files in jar.
- Build with javac -encoding UTF-8.
- Use %%javac and %%jar macros.
- Run test suite during build (ignoring failures for now).
- Follow upstream in excluding various test suite classes from jar.
- Add BR: junit4

* Wed Aug 26 2009 Andrew Overholt <overholt@redhat.com> 1.43-4
- Add maven POM

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.43-2
- Re-enable AOT bits thanks to Andrew Haley.

* Mon Apr 20 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.43-1
- Import Bouncy Castle 1.43.

* Sat Apr 18 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.42-4
- Rebuild

* Sat Apr 18 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.42-3
- Don't build AOT bits. The package needs java1.6

* Thu Apr 09 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.42-2
- Add missing Requires: javamail
- Remove redundant BR: junit4

* Tue Mar 17 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.42-1
- Import Bouncy Castle 1.42.
- Add javadoc subpackage.

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 6 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.41-3
- Added "Provides: bcmail == %%{version}-%%{release}"
- Added "Requires: bouncycastle == %%{version}"

* Sun Oct  5 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.41-2
- Some minor fixes/improvements in the spec file
- Improved Summary/Description
- License is MIT

* Thu Oct  2 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.41-1
- Initial Release
- Spec file stolen from bouncycastle-1.41-1 and modified for bcmail

