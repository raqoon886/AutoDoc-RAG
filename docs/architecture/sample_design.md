# Middleware Architecture Design

## 1. Overview
This middleware is designed to run on Ubuntu systems, providing a lightweight IPC mechanism using D-Bus.

## 2. Components

### Service Manager
The `ServiceManager` is the core component responsible for:
- parsing configuration files.
- managing the lifecycle (start, stop, restart) of the service.
- exposing D-Bus interfaces.

### Configuration
Configuration is loaded from `/etc/middleware/config.json`.
Key parameters include:
- `service_name`: The name registered on the system bus.
- `port`: TCP port for external communication.

## 3. Communication Flow
1.  **Initialization**: The service reads the config and registers the bus name.
2.  **Request Handling**: Incoming D-Bus method calls are routed to the appropriate handler in `ServiceManager`.
