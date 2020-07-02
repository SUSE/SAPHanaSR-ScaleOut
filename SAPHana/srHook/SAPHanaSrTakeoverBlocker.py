from hdb_ha_dr.client import HADRBase
import os, time

fhSRHookVersion = "0.162.0"


class SAPHanaSrTakeoverBlocker(HADRBase):

    def __init__(self, *args, **kwargs):
        # delegate construction to base class
        super(SAPHanaSrTakeoverBlocker, self).__init__(*args, **kwargs)

    def about(self):
        return {"provider_company": "SUSE",
                "provider_name": "SAPHanaSrTakeoverBlocker",  # class name
                "provider_description": "Inform Cluster about SR state",
                "provider_version": "1.0"}

    def startup(self, hostname, storage_partition, sr_mode, **kwargs):
        self.tracer.debug("enter startup hook; %s" % locals())
        self.tracer.debug(self.config.toString())
        self.tracer.info("leave startup hook")
        return 0

    def shutdown(self, hostname, storage_partition, sr_mode, **kwargs):
        self.tracer.debug("enter shutdown hook; %s" % locals())
        self.tracer.debug(self.config.toString())
        self.tracer.info("leave shutdown hook")
        return 0

    def failover(self, hostname, storage_partition, sr_mode, **kwargs):
        self.tracer.debug("enter failover hook; %s" % locals())
        self.tracer.debug(self.config.toString())
        self.tracer.info("leave failover hook")
        return 0

    def stonith(self, failingHost, **kwargs):
        self.tracer.debug("enter stonith hook; %s" % locals())
        self.tracer.debug(self.config.toString())
        # e.g. stonith of params["failed_host"]
        # e-g- set vIP active
        self.tracer.info("leave stonith hook")
        return 0

    def preTakeover(self, isForce, **kwargs):
        """Pre takeover hook."""
        """
           * TODO PRIO1: add check, if cluster does actively manage the resource
           * Prerequisites:
           *    RA does set the same attribute as checked here (key and value)
           *    Sudoers does allow the query of the attribute (alternatively add <sid>adm user(s) to hacluster group)
        """
        self.tracer.info("%s.preTakeover method called with isForce=%s" % (self.__class__.__name__, isForce))
        if not isForce:
            # run pre takeover code
            # run pre-check, return != 0 in case of error => will abort takeover
            # for test purposes just block all sr_takeover() calls
            mySID = os.environ.get('SAPSYSTEMNAME')
            mysid = mySID.lower()
            myAttribute = "hana_" + mysid + "_sra"
            myCMD = "sudo /usr/sbin/crm_attribute -n hana_" + mysid + "_sra -G -t reboot -q"
            self.tracer.info("%s.preTakeover myCMD is: %s" % (self.__class__.__name__, myCMD))
            mySRA = ""
            mySRAres = os.popen(myCMD)
            mySRAlines = list(mySRAres)
            for line in mySRAlines:
                mySRA = mySRA + line
            mySRA = mySRA.rstrip()
            if ( mySRA == "T" ):
               self.tracer.info("%s.preTakeover permit cluster action sr_takeover() sra=%s" % (self.__class__.__name__, mySRA))
               rc = 0
            else:
               self.tracer.info("%s.preTakeover reject non-cluster action sr_takeover() sra=%s" % (self.__class__.__name__, mySRA))
               rc = 1
            return rc
        else:
            # possible force-takeover only code
            # usually nothing to do here
            return 0

    def postTakeover(self, rc, **kwargs):
        """Post takeover hook."""
        self.tracer.info("%s.postTakeover method called with rc=%s" % (self.__class__.__name__, rc))
        if rc == 0:
            # normal takeover succeeded
            return 0
        elif rc == 1:
            # waiting for force takeover
            return 0
        elif rc == 2:
            # error, something went wrong
            return 0

    def srConnectionChanged(self, ParamDict, **kwargs):
        """ This hook should just do nothing for this HA/DR method """
        return 0
