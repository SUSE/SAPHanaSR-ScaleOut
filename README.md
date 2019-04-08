
# SUSE ScaleOut resource agent for SAP HANA

[![Build Status](https://travis-ci.com/SUSE/SAPHanaSR-ScaleOut.svg?branch=master)](https://travis-ci.com/SUSE/SAPHanaSR-ScaleOut)

## Introduction

SAPHanaSR Scale-Out provides an automatic failover between SAP HANA nodes with configured System Replication for complex HANA Scale-Out configurations running in two different locations.

This technology is included in the SUSE Linux Enterprise Server for SAP Applications 12 SP2 or later, via the RPM package with the same name.

System replication will help to replicate the database data from one site to another site in order to compensate for database failures. With this mode of operation, internal SAP HANA high-availability (HA) mechanisms and the Linux cluster have to work together.

An HANA scale-out setup already is, to some degree, an HA cluster on its own. The HANA is able to replace failing nodes with standby nodes or to restart certain sub-systems on other nodes. As long as the HANA landscape status is not "ERROR" the Linux cluster will not act. The main purpose of the Linux cluster is to handle the take-over to the other site. 

Only if the HANA landscape status indicates that HANA can not recover from the failure and the replication is in sync, then Linux cluster will act. As an exception, the Linux cluster will react if HANA moves the master nameserver role to another candidate. 

SAPHanaController is also able to restart former failed worker nodes as standby. In addition to the SAPHanaTopology RA, the SAPHanaSR-ScaleOut solution uses a
"HA/DR providers" API provided by HANA to get informed about the current state of the system replication.

For more information, refer to the ["SAP HANA System Replication Scale-Out - Performance Optimized Scenario" Best Practices guide](https://www.suse.com/documentation/suse-best-practices/singlehtml/SLES4SAP-hana-scaleOut-PerfOpt-12/SLES4SAP-hana-scaleOut-PerfOpt-12.html)

**Note:** To automate SAP HANA SR in scale-up setups, please use the package SAPHanaSR instead.


## License

See the [LICENSE](LICENSE) file for license rights and limitations.


## Contributing

If you are interested in contributing to this project, read the [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

## Feedback
Do you have suggestions for improvement? Let us know!

Go to Issues, create a [new issue](https://github.com/SUSE/SAPHanaSR-ScaleOut/issues) and describe what you think could be improved.

Feedback is always welcome!