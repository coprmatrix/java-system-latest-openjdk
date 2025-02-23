%global featurever latest
%global origin          openjdk
%global java java-system

BuildArch: noarch
BuildRequires: javapackages-filesystem
BuildRequires: rpm
BuildRequires: java-%{featurever}-%{origin}
BuildRequires: grep
BuildRequires: sed

Name: %{java}-%{featurever}-%{origin}
%(rpm  --queryformat 'Version: %%{version}\nRelease: %%{release}\nEpoch: %%{epoch}\nRequires: %%{name} = %%{epoch}:%%{version}-%%{release}\nSummary: %%{summary}\nLicense: %%{license}\nURL: %%{url}' -q java-%{featurever}-%{origin} | sed 's/.*is not installed.*/Version: 0\nRelease: 0\nEpoch: 0\nSummary: sum\nLicense: lic/' )

#placeholder - used in regexes, otherwise for no use in portables
%global freetype_lib |libfreetype[.]so.*
# Standard JPackage naming and versioning defines
%global origin_nice     OpenJDK
%global _publiclibs libjawt[.]so.*|libjava[.]so.*|libjvm[.]so.*|libverify[.]so.*|libjsig[.]so.*
%global alt_java_name     alt-java
%global javaver %(echo %{version} | sed 's~[.].*~~')

%define files_jre_headless() %{expand:
%ghost %{_bindir}/java
%ghost %{_jvmdir}/jre
%ghost %{_bindir}/%{alt_java_name}
%ghost %{_bindir}/jcmd
%ghost %{_bindir}/keytool
%ghost %{_bindir}/rmiregistry
%ghost %{_jvmdir}/jre-%{origin}
%ghost %{_jvmdir}/jre-%{javaver}
%ghost %{_jvmdir}/jre-%{javaver}-%{origin}
}

%define files_devel() %{expand:
%ghost %{_bindir}/javac
%ghost %{_jvmdir}/java
%ghost %{_jvmdir}/%{alt_java_name}
%ghost %{_bindir}/jlink
%ghost %{_bindir}/jmod
%ghost %{_bindir}/jhsdb
%ghost %{_bindir}/jar
%ghost %{_bindir}/jarsigner
%ghost %{_bindir}/javadoc
%ghost %{_bindir}/javap
%ghost %{_bindir}/jconsole
%ghost %{_bindir}/jcmd
%ghost %{_bindir}/jdb
%ghost %{_bindir}/jdeps
%ghost %{_bindir}/jdeprscan
%ghost %{_bindir}/jfr
%ghost %{_bindir}/jimage
%ghost %{_bindir}/jinfo
%ghost %{_bindir}/jmap
%ghost %{_bindir}/jps
%ghost %{_bindir}/jpackage
%ghost %{_bindir}/jrunscript
%ghost %{_bindir}/jshell
%ghost %{_bindir}/jstack
%ghost %{_bindir}/jstat
%ghost %{_bindir}/jstatd
%ghost %{_bindir}/jwebserver
%ghost %{_bindir}/serialver
%ghost %{_jvmdir}/java-%{origin}
%ghost %{_jvmdir}/java-%{javaver}
}

%define files_javadoc() %{expand:
%ghost %{_javadocdir}/java
%ghost %{_javadocdir}/java-%{origin}
%ghost %{_javadocdir}/java-%{javaver}
}

%define files_javadoc_zip() %{expand:
%ghost %{_javadocdir}/java-zip
%ghost %{_javadocdir}/java-%{origin}.zip
%ghost %{_javadocdir}/java-%{javaver}.zip
}

# not-duplicated requires/provides/obsoletes for normal/debug packages
%define java_rpo() %{expand:
Provides: java-%{origin}%{?1} = %{epoch}:%{version}-%{release}
Provides: jre-%{origin}%{?1} = %{epoch}:%{version}-%{release}
Provides: java%{?1} = %{epoch}:%{version}-%{release}
Provides: jre%{?1} = %{epoch}:%{version}-%{release}

%(rpm  --list -q java-%{featurever}-%{origin} | grep -E '%{_publiclibs}' | %{_rpmconfigdir}/find-provides | sed 's~^~Provides: ~;s~.*is not installed.*~~;' )

}

%define java_headless_rpo() %{expand:
Provides: java-%{origin}-headless%{?1} = %{epoch}:%{version}-%{release}
Provides: jre-%{origin}-headless%{?1} = %{epoch}:%{version}-%{release}
Provides: jre-headless%{?1} = %{epoch}:%{version}-%{release}
Provides: java-headless%{?1} = %{epoch}:%{version}-%{release}

%(rpm  --list -q java-%{featurever}-%{origin}-headless | grep -E '%{_publiclibs}' | %{_rpmconfigdir}/find-provides | sed  's~^~Provides: ~;s~.*is not installed.*~~;' )

}

%define java_devel_rpo() %{expand:
Provides: java-devel-%{origin}%{?1} = %{epoch}:%{version}-%{release}
Provides: java-sdk-%{origin}%{?1} = %{epoch}:%{version}-%{release}
Provides: java-devel%{?1} = %{epoch}:%{version}-%{release}
Provides: java-sdk%{?1} = %{epoch}:%{version}-%{release}
}

%define java_jmods_rpo() %{expand:
Provides: java-jmods%{?1} = %{epoch}:%{version}-%{release}
}

%define java_demo_rpo() %{expand:
Provides: java-demo%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{origin}-demo%{?1} = %{epoch}:%{version}-%{release}
}

%define java_javadoc_rpo() %{expand:
Provides: java-javadoc%{?1}%{?2} = %{epoch}:%{version}-%{release}
}

%define java_src_rpo() %{expand:
Provides: java-src%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{origin}-src%{?1} = %{epoch}:%{version}-%{release}
}

# Prevent brp-java-repack-jars from being run
%global __jar_repack 0

%global portable_name %{name}-portable
# the version must match, but sometmes we need to more precise, so including release
%global portable_version %{version}-1

%{?java_rpo %{nil}}

%description
%(rpm  --queryformat '%%{description}' -q java-%{featurever}-%{origin})


%package -n %{java}-%{featurever}-%{origin}-headless
Summary: %{origin_nice} %{featurever} Headless Runtime Environment
Requires: java-%{featurever}-%{origin}-headless = %{epoch}:%{version}-%{release}

%{?java_headless_rpo %{nil}}

%description -n %{java}-%{featurever}-%{origin}-headless
The %{origin_nice} %{featurever} runtime environment without audio and video support.


%package -n %{java}-%{featurever}-%{origin}-devel
Summary: %{origin_nice} %{featurever} Development Environment
Requires: java-%{featurever}-%{origin}-devel = %{epoch}:%{version}-%{release}

%{?java_devel_rpo %{nil}}

%description -n %{java}-%{featurever}-%{origin}-devel
The %{origin_nice} %{featurever} development tools.

%package -n %{java}-%{featurever}-%{origin}-static-libs
Summary: %{origin_nice} %{featurever} libraries for static linking
Requires: java-%{featurever}-%{origin}-static-libs = %{epoch}:%{version}-%{release}

%{?java_static_libs_rpo %{nil}}

%description -n %{java}-%{featurever}-%{origin}-static-libs
The %{origin_nice} %{featurever} libraries for static linking.

%package -n %{java}-%{featurever}-%{origin}-jmods
Summary: JMods for %{origin_nice} %{featurever}
Requires: java-%{featurever}-%{origin}-jmods = %{epoch}:%{version}-%{release}

%{?java_jmods_rpo %{nil}}

%description -n %{java}-%{featurever}-%{origin}-jmods
The JMods for %{origin_nice} %{featurever}.

%package -n %{java}-%{featurever}-%{origin}-demo
Summary: %{origin_nice} %{featurever} Demos
Requires: java-%{featurever}-%{origin}-demo = %{epoch}:%{version}-%{release}

%{?java_demo_rpo %{nil}}

%description -n %{java}-%{featurever}-%{origin}-demo
The %{origin_nice} %{featurever} demos.

%package -n %{java}-%{featurever}-%{origin}-src
Summary: %{origin_nice} %{featurever} Source Bundle
Requires: java-%{featurever}-%{origin}-src = %{epoch}:%{version}-%{release}

%{?java_src_rpo %{nil}}

%description -n %{java}-%{featurever}-%{origin}-src
The %{compatiblename}-src sub-package contains the complete %{origin_nice} %{featurever}
class library source code for use by IDE indexers and debuggers.

%package -n %{java}-%{featurever}-%{origin}-javadoc
Summary: %{origin_nice} %{featurever} API documentation
Requires: java-%{featurever}-%{origin}-javadoc = %{epoch}:%{version}-%{release}

%{?java_javadoc_rpo %{nil}}

%description -n %{java}-%{featurever}-%{origin}-javadoc
The %{origin_nice} %{featurever} API documentation.

%package -n %{java}-%{featurever}-%{origin}-javadoc-zip
Summary: %{origin_nice} %{featurever} API documentation compressed in a single archive
Requires: java-%{featurever}-%{origin}-javadoc-zip = %{epoch}:%{version}-%{release}

%{?java_javadoc_rpo}

%description -n %{java}-%{featurever}-%{origin}-javadoc-zip
The %{origin_nice} %{featurever} API documentation compressed in a single archive.

%files
# main package builds always
%{?files_jre %{nil}}

%files -n %{java}-%{featurever}-%{origin}-headless
%{?files_jre_headless %{nil}}

%files -n %{java}-%{featurever}-%{origin}-devel
%{?files_devel %{nil}}

%files -n %{java}-%{featurever}-%{origin}-static-libs
%{?files_static_libs %{nil}}

%files -n %{java}-%{featurever}-%{origin}-jmods
%{?files_jmods %{nil}}

%files -n %{java}-%{featurever}-%{origin}-demo
%{?files_demo %{nil}}

%files -n %{java}-%{featurever}-%{origin}-src
%{?files_src %{nil}}

%files -n %{java}-%{featurever}-%{origin}-javadoc
%{?files_javadoc %{nil}}

%files -n %{java}-%{featurever}-%{origin}-javadoc-zip
%{?files_javadoc_zip %{nil}}

%changelog
%autochangelog
