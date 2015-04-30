RADIR = /usr/lib/ocf/resource.d/suse

install:
	mkdir -p $(RADIR)
	install SAPHana $(RADIR)/SAPHana.stage
	install SAPHanaTopology $(RADIR)/SAPHanaTopology.stage
	mv $(RADIR)/SAPHana.stage $(RADIR)/SAPHana
	mv $(RADIR)/SAPHanaTopology.stage $(RADIR)/SAPHanaTopology
	mkdir -p /usr/share/SAPHanaSR/tests
	install show_SAPHanaSR_attributes /usr/share/SAPHanaSR/tests/show_SAPHanaSR_attributes
	install fh_mini_mon /usr/sbin/fh_mini_mon
	install fh_test_driver-scale-out /usr/sbin/fh_test_driver-scale-out
	install SAPHanaSR-monitor /usr/sbin/SAPHanaSR-monitor
