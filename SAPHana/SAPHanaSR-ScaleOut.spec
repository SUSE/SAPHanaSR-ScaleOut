#
# spec file for package SAPHanaSR-ScaleOut
#
# Copyright (c) 2016      SUSE LINUX GmbH, Nuernberg, Germany.
# Copyright (c) 2017-2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:           SAPHanaSR-ScaleOut
License:        GPL-2.0
Group:          Productivity/Clustering/HA
AutoReqProv:    on
Summary:        Resource agents to control the HANA database in system replication setup
Version:        0.180.0
Release:        0
Url:            http://scn.sap.com/community/hana-in-memory/blog/2014/04/04/fail-safe-operation-of-sap-hana-suse-extends-its-high-availability-solution
Source0:        SAPHanaSR-ScaleOut-%{version}.tar.bz2

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

Requires:       pacemaker > 1.1.1
Requires:       resource-agents
Requires:       perl
Requires:       python3
Requires:       /usr/bin/xmllint
Conflicts:      SAPHanaSR

%package doc
Summary:        Setup-Guide for SAPHanaSR
Group:          Productivity/Clustering/HA
Conflicts:      SAPHanaSR-doc

%description
The resource agents SAPHana and SAPHanaTopology are responsible for controlling a SAP HANA Database which is
running in system replication (SR) configuration.

For SAP HANA Databases in System Replication only the described or referenced scenarios in the README file of
this package are supported. For any scenario not matching the scenarios named or referenced in the README file
please contact SUSE at SAP LinuxLab (sap-lab@suse.de).

The following SCN blog gives a first overwiew about running SAP HANA in system replication with our resource agents:
http://scn.sap.com/community/hana-in-memory/blog/2014/04/04/fail-safe-operation-of-sap-hana-suse-extends-its-high-availability-solution



Authors:
--------
    Fabian Herschel

%description doc
This sub package includes the Setup-Guide for getting SAP HANA system replication under cluster control.

%prep
tar xf %{S:0}

%build
gzip man/*

%install
mkdir -p %{buildroot}/usr/sbin
mkdir -p %{buildroot}%{_docdir}/%{name}
mkdir -p %{buildroot}/usr/share/%{name}/tests
mkdir -p %{buildroot}/usr/share/%{name}/samples
mkdir -p %{buildroot}%{_mandir}/man7
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}/usr/lib/ocf/resource.d/suse/

# resource agents
install -m 0755 ra/* %{buildroot}/usr/lib/ocf/resource.d/suse/

# documentation
install -m 0444 doc/* %{buildroot}/%{_docdir}/%{name}

# manuals
install -m 0444 man/*.7.gz %{buildroot}/usr/share/man/man7
install -m 0444 man/*.8.gz %{buildroot}/usr/share/man/man8

# aux. scripts
#    SAPHanaSR-showAttr, SAPHanaSR-monitor
install -m 0555 bin/* %{buildroot}/usr/sbin
install -m 0555 test/SAPHanaSR-replay-archive %{buildroot}/usr/sbin
install -m 0555 test/SAPHanaSR-filter %{buildroot}/usr/sbin
install -Dm 0444 test/SAPHanaSRTools.pm %{buildroot}/usr/lib/%{name}/SAPHanaSRTools.pm

# sample configurations
install -m 0444 crmconfig/* %{buildroot}/usr/share/%{name}/samples

# HAWK components
install -Dm 0444 wizard/templates/SAPHanaSR-ScaleOut.xml %{buildroot}/srv/www/hawk/config/wizard/templates/SAPHanaSR-ScaleOut.xml
install -Dm 0444 wizard/workflows/90-SAPHanaSR-ScaleOut.xml  %{buildroot}/srv/www/hawk/config/wizard/workflows/90-SAPHanaSR-ScaleOut.xml

# HANA hooks
install -m 0644 srHook/SAPHanaSR.py %{buildroot}/usr/share/%{name}/
install -m 0644 srHook/SAPHanaSrMultiTarget.py %{buildroot}/usr/share/%{name}/
install -m 0444 srHook/global.ini %{buildroot}/usr/share/%{name}/samples
install -m 0444 srHook/sudoers %{buildroot}/usr/share/%{name}/samples

%files
%defattr(-,root,root)
%dir /usr/lib/ocf
%dir /usr/lib/ocf/resource.d
%dir /usr/lib/ocf/resource.d/suse
/usr/lib/ocf/resource.d/suse/SAPHanaController
/usr/lib/ocf/resource.d/suse/SAPHanaTopology
/usr/share/%{name}
/usr/lib/%{name}
/usr/sbin/SAPHanaSR-monitor
/usr/sbin/SAPHanaSR-showAttr
/usr/sbin/SAPHanaSR-manageAttr
/usr/sbin/SAPHanaSR-replay-archive
/usr/sbin/SAPHanaSR-filter
%dir /srv/www/hawk
%dir /srv/www/hawk/config
%dir /srv/www/hawk/config/wizard
%dir /srv/www/hawk/config/wizard/templates
%dir /srv/www/hawk/config/wizard/workflows
/srv/www/hawk/config/wizard/templates/SAPHanaSR-ScaleOut.xml
/srv/www/hawk/config/wizard/workflows/90-SAPHanaSR-ScaleOut.xml
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/README
%doc %{_docdir}/%{name}/LICENSE
%doc %{_mandir}/man7/*
%doc %{_mandir}/man8/*

%files doc
%defattr(-,root,root)
%doc %{_docdir}/%{name}/SAPHanaSR-Setup-Guide.pdf

%changelog
