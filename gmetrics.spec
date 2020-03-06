Name:          gmetrics
Version:       0.7
Release:       6
Summary:       Library for Groovy
License:       ASL 2.0
Url:           http://gmetrics.sourceforge.net/
Source0:       http://downloads.sourceforge.net/%{name}/GMetrics-%{version}-bin.tar.gz

BuildRequires: maven-local mvn(junit:junit) mvn(log4j:log4j:12) mvn(org.apache.ant:ant)
BuildRequires: mvn(org.codehaus.gmavenplus:gmavenplus-plugin) mvn(org.codehaus.groovy:groovy)
BuildRequires: mvn(org.codehaus.groovy:groovy-ant) mvn(org.codehaus.groovy:groovy-xml)
BuildRequires: mvn(org.codehaus.groovy:groovy-test) mvn(org.sonatype.oss:oss-parent:pom:)

BuildArch:     noarch

%description
The GMetrics project provides calculation and reporting of size and complexity metrics for Groovy
source code, by scanning the code with an Ant Task, applying a set of metrics, and generating an
HTML or XML report of the results.

%package       help
Summary:       API docs for %{name}
Provides:      %{name}-javadoc = %{version}-%{release}
Obsoletes:     %{name}-javadoc < %{version}-%{release}

%description   help
The package provides API documents for %{name}.

%prep
%autosetup -p1 -n GMetrics-%{version}

find -name "*.jar" -delete -or -name "*.class" -delete
rm -rf docs/*

%pom_remove_plugin :maven-assembly-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-release-plugin
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :gmaven-plugin
%pom_add_plugin org.codehaus.gmavenplus:gmavenplus-plugin:1.5 . "
 <executions>
  <execution>
   <goals>
    <goal>generateStubs</goal>
    <goal>testGenerateStubs</goal>
   </goals>
  </execution>
 </executions>"

%pom_remove_dep :CodeNarc
%pom_change_dep :log4j ::12

%pom_add_dep org.apache.ant:ant:1.9.6 . "<optional>true</optional>"

chmod 644 README.txt

for text in CHANGELOG.txt LICENSE.txt NOTICE.txt README.txt
do
    sed -i.orig 's|\r||g' $text
    touch -r $text.orig $text
    rm -f $text.orig
done

%mvn_file :GMetrics %{name} GMetrics

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc CHANGELOG.txt README.txt
%license LICENSE.txt NOTICE.txt

%files help -f .mfiles-javadoc

%changelog
* Wed Mar 4 2020 zhouyihang<zhouyihang1@huawei.com> - 0.7-6
- Pakcage init
