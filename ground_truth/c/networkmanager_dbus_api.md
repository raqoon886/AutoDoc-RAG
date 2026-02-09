# org.freedesktop.NetworkManager — D-Bus API Reference

> Source: https://networkmanager.dev/docs/api/latest/gdbus-org.freedesktop.NetworkManager.html

## Description
org.freedesktop.NetworkManager — Connection Manager.

## Methods

### Reload (IN u flags)
Reload NetworkManager's configuration and perform certain updates. This is similar to sending SIGHUP but allows fine-grained control.

**Parameters:**
- `flags` (u): Optional flags to specify which parts shall be reloaded.
  - 0x00: Reload everything (same as SIGHUP)
  - 0x01: Reload NetworkManager.conf configuration
  - 0x02: Update DNS configuration (writes /etc/resolv.conf)
  - 0x04: Restart the DNS plugin

### GetDevices (OUT ao devices)
Get the list of realized network devices.

**Returns:**
- `devices` (ao): List of object paths of network devices known to the system.

### GetAllDevices (OUT ao devices)
Get the list of all network devices, including device placeholders.

**Returns:**
- `devices` (ao): List of object paths of network devices and device placeholders.

### GetDeviceByIpIface (IN s iface, OUT o device)
Return the object path of the network device referenced by its IP interface name.

**Parameters:**
- `iface` (s): Interface name of the device to find.

**Returns:**
- `device` (o): Object path of the network device.

### ActivateConnection (IN o connection, IN o device, IN o specific_object, OUT o active_connection)
Activate a connection using the supplied device.

**Parameters:**
- `connection` (o): The connection to activate. Use "/" for auto-selection.
- `device` (o): Object path of device (ignored for VPN).
- `specific_object` (o): Connection-type-specific object (e.g., AP for Wi-Fi).

**Returns:**
- `active_connection` (o): Path of the active connection object.

### DeactivateConnection (IN o active_connection)
Deactivate an active connection.

### Sleep (IN b sleep)
Control the sleep mode of NetworkManager.

### Enable (IN b enable)
Enable or disable networking.

### CheckConnectivity (OUT u connectivity)
Re-check the connectivity state of NetworkManager.

### CheckpointCreate (IN ao devices, IN u rollback_timeout, IN u flags, OUT o checkpoint)
Create a configuration checkpoint for specified devices.

### CheckpointRollback (IN o checkpoint, OUT a{su} result)
Rollback to a previously created checkpoint.

---

## Properties

### Devices (readable ao)
The list of realized network devices.

### AllDevices (readable ao)
The list of both realized and un-realized network devices.

### NetworkingEnabled (readable b)
Indicates if overall networking is currently enabled.

### WirelessEnabled (readwrite b)
Indicates if wireless is currently enabled.

### ActiveConnections (readable ao)
List of active connection object paths.

### PrimaryConnection (readable o)
The object path of the "primary" active connection.

### State (readable u)
Overall state of the NetworkManager daemon.

### Connectivity (readable u)
Current network connectivity state.

### Version (readable s)
NetworkManager version.

---

## Signals

### CheckPermissions
Emitted when permissions might have changed.

### StateChanged (u state)
Emitted when the overall state changes.

### DeviceAdded (o device)
Emitted when a new device is added.

### DeviceRemoved (o device)
Emitted when a device is removed.
