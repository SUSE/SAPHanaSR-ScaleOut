"""
# SAPHana
# Author:       Fabian Herschel, 2015
# License:      GNU General Public License (GPL)
# Copyright:    (c) 2015-2016 SUSE Linux GmbH
# Copyright:    (c) 2017-2022 SUSE LLC
"""
try:
    from hdb_ha_dr.client import HADRBase
except ImportError as e:
    print("Module HADRBase not found - running outside of SAP HANA? - {0}".format(e))
import os

"""
Sample for a HA/DR hook provider.
When using your own code in here, please copy this file to location on
/hana/shared outside the HANA installation.
To use this HA/DR hook provide please add the following lines (or
similar) to your global.ini:
    [ha_dr_provider_SAPHanaSR]
    provider = SAPHanaSR
    path = /usr/share/SAPHanaSR-ScaleOut
    execution_order = 1

    [trace]
    ha_dr_saphanasr = info
"""
fhSRHookVersion = "0.184.1"
srHookGen = "1.0"


try:
    class SAPHanaSR(HADRBase):

        def __init__(self, *args, **kwargs):
            # delegate construction to base class
            super(SAPHanaSR, self).__init__(*args, **kwargs)
            method = "init"
            self.tracer.info("{0}.{1}() version {2}".format(self.__class__.__name__, method, fhSRHookVersion))
            mySID = os.environ.get('SAPSYSTEMNAME')
            mysid = mySID.lower()
            myCMD = "sudo /usr/sbin/crm_attribute -n hana_{1}_gsh -v {0} -l reboot".format(srHookGen, mysid)
            rc = os.system(myCMD)
            myMSG = "CALLING CRM: <{0}> rc={1}".format(myCMD, rc)
            self.tracer.info("{0}.{1}() {2}\n".format(self.__class__.__name__, method, myMSG))
            self.tracer.info("{0}.{1}() Running old srHookGeneration {2}, see attribute hana_{3}_gsh too\n".format(self.__class__.__name__, method, srHookGen, mysid))

        def about(self):
            return {"provider_company": "SUSE",
                    "provider_name": "SAPHanaSR",  # class name
                    "provider_description": "Inform Cluster about SR state",
                    "provider_version": "1.0"}

        def srConnectionChanged(self, ParamDict, **kwargs):
            """ finally we got the srConnection hook :) """
            method = "srConnectionChanged"
            self.tracer.info("SAPHanaSR (%s) %s.srConnectionChanged method called with Dict=%s" % (fhSRHookVersion, self.__class__.__name__, ParamDict))
            # myHostname = socket.gethostname()
            # myDatebase = ParamDict["database"]
            mySystemStatus = ParamDict["system_status"]
            mySID = os.environ.get('SAPSYSTEMNAME')
            mysid = mySID.lower()
            myInSync = ParamDict["is_in_sync"]
            myReason = ParamDict["reason"]
            myCMD = "sudo /usr/sbin/crm_attribute -n hana_{1}_gsh -v {0} -l reboot".format(srHookGen, mysid)
            rc = os.system(myCMD)
            myMSG = "CALLING CRM: <{0}> rc={1}".format(myCMD, rc)
            self.tracer.info("{0}.{1}() {2}\n".format(self.__class__.__name__, method, myMSG))
            self.tracer.info("{0}.{1}() Running old srHookGeneration {2}, see attribute hana_{3}_gsh too\n".format(self.__class__.__name__, method, srHookGen, mysid))
            if mySystemStatus == 15:
                mySRS = "SOK"
            else:
                if myInSync:
                    # ignoring the SFAIL, because we are still in sync
                    self.tracer.info("SAPHanaSR (%s) %s.srConnectionChanged ignoring bad SR status because of is_in_sync=True (reason=%s)" % (fhSRHookVersion, self.__class__.__name__, myReason))
                    mySRS = ""
                else:
                    mySRS = "SFAIL"
            if mySRS == "":
                self.tracer.info("SAPHanaSR (%s) 001" % (self.__class__.__name__))
                myMSG = "### Ignoring bad SR status because of is_in_sync=True ###"
                self.tracer.info("SAPHanaSR (%s) 002" % (self.__class__.__name__))
            else:
                myCMD = "sudo /usr/sbin/crm_attribute -n hana_%s_glob_srHook -v %s -t crm_config -s SAPHanaSR" % (mysid, mySRS)
                rc = os.system(myCMD)
                myMSG = "CALLING CRM: <" + myCMD + "> rc=" + str(rc)
            self.tracer.info("SAPHanaSR %s.srConnectionChanged method called with Dict=%s ###\n" % (self.__class__.__name__, ParamDict))
            self.tracer.info("SAPHanaSR %s \n" % (myMSG))
            return 0
except NameError as e:
    print("Could not find base class ({0})".format(e))
