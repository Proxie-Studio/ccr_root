# CCR Project Repository

This repository contains all components related to the **CCR (Coordinated Control and Reasoning)** system. The project integrates robotic agents, smart infrastructure, and a centralized dashboard using MQTT-based communication to simulate and manage intelligent traffic and coordination systems.

## Repository Structure

```
/
├── CCR_Central_Hub_Implementation/ # Core Android APK and Arduino code for traffic light simulation
├── CCR_Main_Package/ # Dashboard, MQTT logic, and connected device logic (e.g., TurtleBot, Traffic Lights)
├── Shared_Resources/ # Shared documents, architecture diagrams, and configuration files
├── Vision_Module/ # Computer vision tool setup and integration
```

---

### `CCR_Central_Hub_Implementation/`

- Contains the **CCR Android application (APK)** for traffic control interfaces.
- Includes **Arduino code** to run the ESP32-based traffic light hardware used in simulation.
- Useful for mobile control or simulation-based visualization of intersection states.

---

### `CCR_Main_Package/`

- Implements the **main dashboard**, hosted on a central Ubuntu server.
- Contains device logic for:
  - **Traffic Lights** 
  - **TurtleBot agents**
- All devices publish their status and receive commands through an **MQTT broker**.
- Central hub for real-time monitoring and decision visualization.

---

### `Shared_Resources/`

- Contains supporting files for the project:
  - System architecture diagrams
  - Configuration files
- Acts as a reference and documentation archive.

---

### `Vision_Module/`

- Tools and setup scripts for integrating **computer vision** into the system.
- Used for image-based agent recognition and camera processing.
- May include OpenCV/PyTorch scripts and setup guides for GPU acceleration.

---

## Getting Started

Refer to the individual `README.md` files within each folder for detailed setup instructions, dependencies, and usage notes.

---

## Requirements

- Ubuntu 20.04 or later (for central hub hosting)
- MQTT broker (e.g., Mosquitto)
- Android device (for APK), TurtleBot hardware, USB webcams

---


