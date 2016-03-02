""" 
Sample for a HA/DR hook provider. 
When using your own code in here, please copy this file to location on /hana/shared outside the HANA installation. 
This file will be overwritten with each hdbupd call! To configure your own changed version of this file, please add 
to your global.ini lines similar to this: 
    [ha_dr_provider_<className>] 
    provider = <className> 
    path = /hana/shared/haHook 
    execution_order = 1 
For all hooks, 0 must be returned in case of success. 
Set the following variables : dbinst Instance Number [e.g. 00 - 99 ] 
                              dbuser Username [ e.g. SYSTEM ] 
                              dbpwd  user password [ e.g. SLES4sap ] 
                              dbport port where db listens for sql [e.g 30013 or 30015] 
"""  
fhSRHookVersion="0.160.1"
from hdb_ha_dr.client import HADRBase, Helper 
"""import os, time, dbapi, """
import os, time, socket, subprocess
class SAPHanaSR(HADRBase):  
    def __init__(self, *args, **kwargs):  
        # delegate construction to base class  
        super(SAPHanaSR, self).__init__(*args, **kwargs)  
    def about(self):  
        return {"provider_company" :      "SUSE",  
                "provider_name" :          "SAPHanaSR", # provider name = class name  
                "provider_description" :  "Replication takeover script to set parameters to default.",  
                "provider_version" :      "1.0"}  
    def startup(self, hostname, storage_partition, system_replication_mode, **kwargs):  
        self.tracer.debug("enter startup hook; %s" % locals())  
        self.tracer.debug(self.config.toString())  
        self.tracer.info("leave startup hook")  
        return 0  
    def shutdown(self, hostname, storage_partition, system_replication_mode, **kwargs):  
        self.tracer.debug("enter shutdown hook; %s" % locals())  
        self.tracer.debug(self.config.toString())  
        self.tracer.info("leave shutdown hook")  
        return 0  
    def failover(self, hostname, storage_partition, system_replication_mode, **kwargs):  
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
        self.tracer.info("%s.preTakeover method called with isForce=%s" % (self.__class__.__name__, isForce))  
        if not isForce:  
            # run pre takeover code  
            # run pre-check, return != 0 in case of error => will abort takeover  
            return 0  
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
        """ finally we got the srConnection hook :) """
        self.tracer.info("SAPHanaSR (%s) %s.srConnectionChanged method called with Dict=%s" % (fhSRHookVersion, self.__class__.__name__, ParamDict))
        myHostname = socket.gethostname()
        myLogFile = "/hana/shared/srHook/srHook." + myHostname + ".log"
        myDatebase = ParamDict["database"];
        mySystemStatus = ParamDict["system_status"];
        mySID = os.environ.get('SAPSYSTEMNAME')
        mysid = mySID.lower()
        myInSync = ParamDict["is_in_sync"];
        if ( mySystemStatus == 15 ):
            mySRS="SOK"
        else:
            if ( myInSync ):
                # ignoring the SFAIL, because we are still in sync
                self.tracer.info("SAPHanaSR (%s) %s.srConnectionChanged ignoring bad SR status because of is_in_sync=True" % (self.__class__.__name__))
                mySRS=""
            else:
                mySRS="SFAIL"
        if ( myCMD != "" ):
	    myCMD="sudo /usr/sbin/crm_attribute -n hana_%s_glob_srHook -v %s -t crm_config -s SAPHanaSR" % ( mysid, mySRS )
	    rc=subprocess.call(myCMD.split())
            myMSG="CALLING: <" + myCMD + "> rc=" + str(rc)
        else:
            myMSG="### Ignoring bad SR status because of is_in_sync=True ###"
        with open(myLogFile, "a") as myfile:
            myfile.write("### %s.srConnectionChanged method called with Dict=%s ###\n" % (self.__class__.__name__, ParamDict))
            myfile.write("### %s \n" % (myMSG))
        return 0
