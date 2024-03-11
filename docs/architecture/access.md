---
title: Workspace ONE Access Architecture
draft: false
date: 2024-03-01
authors:
  - rcroft-work
---

## Cloud-Based Architecture

In a cloud-based implementation, the Workspace ONE Access Connector service synchronizes user accounts from Active Directory to the Workspace ONE Access tenant service. Applications can then be accessed from a cloud-based entry point.

![44408-0724-145915-3](https://images.techzone.vmware.com/sites/default/files/imported-images/node_2940_0724-145921/44408-0724-145915/44408-0724-145915-3.png)

The main components of a cloud-based Workspace ONE Access implementation are described in the following table.

Table 2: Workspace ONE Access Components

|Component | Description |
|---|---|
|Workspace ONE Access tenant | Hosted in the cloud and runs the main Workspace ONE Access service. |
|Workspace ONE Access Connector | Responsible for directory synchronization and handles some of the authentication methods between on-premises resources such as Active Directory, VMware Horizon, Citrix, and the Workspace ONE Access service. |

## On-Premises Architecture

For the on-premises deployment, we use the Linux-based virtual appliance version of the Workspace ONE Access service. This appliance is often deployed to the DMZ. There are use cases for LAN deployment, but they are rare, and we focus on the most common deployment method in this guide.

Syncing resources such as Active Directory, Citrix apps and desktops, and Horizon desktops and published apps is done by using a separate Workspace ONE Access Connector. The Workspace ONE Access Connector runs inside the LAN using an outbound-only connection to the Workspace ONE Access service, meaning the connector receives no incoming connections from the DMZ or from the Internet.

![44408-0724-145915-5](https://images.techzone.vmware.com/sites/default/files/imported-images/node_2940_0724-145921/44408-0724-145915/44408-0724-145915-5.png)
The implementation is separated into three main components.

|Component | Description|
|---|---|
|Workspace ONE Access appliance | Runs the main Workspace ONE Access Service.<br/>The Workspace ONE Access Service is a virtual appliance (OVA file) that you deploy in a VMware vSphere® environment.|
|Workspace ONE Access Connector | Performs directory synchronization and authentication between on-premises resources such as Active Directory, VMware Horizon, and the Workspace ONE Access service.<br/>You deploy the connector by running a Windows-based installer.|
|Database | Stores and organizes server-state data and user account data.|

Learn more about how Workspace ONE Access works, what to consider, and how to design deployments by reviewing the [Workspace ONE Access Architecture](https://techzone.vmware.com/resource/workspace-one-access-architecture).
