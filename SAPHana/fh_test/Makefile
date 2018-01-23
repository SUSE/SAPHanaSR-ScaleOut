RADIR = /usr/lib/ocf/resource.d/suse

install:
	mkdir -p $(RADIR)
	install SAPHana $(RADIR)/SAPHana.stage
	install SAPHanaTopology $(RADIR)/SAPHanaTopology.stage
	mv $(RADIR)/SAPHana.stage $(RADIR)/SAPHana
	mv $(RADIR)/SAPHanaTopology.stage $(RADIR)/SAPHanaTopology
	mkdir -p /usr/share/SAPHanaSR/tests
	install SAPHanaSR-checks /usr/sbin/SAPHanaSR-checks
	install SAPHanaSR-miniMon /usr/sbin/SAPHanaSR-miniMon
	install SAPHanaSR-monitor /usr/sbin/SAPHanaSR-monitor
	install SAPHanaSR-showAttr /usr/sbin/SAPHanaSR-showAttr
	install SAPHanaSR-testDriver /usr/sbin/SAPHanaSR-testDriver
	install SAPHanaSRTools.pm /usr/lib/perl5/vendor_perl/5.10.0/SAPHanaSRTools.pm
	ln -s /usr/sbin/SAPHanaSR-miniMon /usr/sbin/fh_mini_mon
	ln -s /usr/sbin/SAPHanaSR-showAttr /usr/share/SAPHanaSR/tests/show_SAPHanaSR_attributes
	ln -s /usr/sbin/SAPHanaSR-testDriver /usr/sbin/fh_test_driver-scale-out
