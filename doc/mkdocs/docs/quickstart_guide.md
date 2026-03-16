# ergoCub-S/N:003 - Quickstart Guide

## Introduction

**ergoCub** is an open-source humanoid robot platform derived from the iCub architecture, specifically designed and enhanced for industrial applications, collaborative robotics, and advanced research. Unlike iCub which focuses on cognitive science and developmental robotics, ergoCub emphasizes robustness, modularity, and practical deployment in real-world environments.

It represents a fully-electrified humanoid with 45 degrees of freedom distributed across the head, torso, and limbs. The robot leverages a distributed embedded control architecture with multiple Ethernet-connected boards for real-time motor control, comprehensive proprioceptive and exteroceptive sensing, and a robust YARP (Yet Another Robot Platform) middleware stack for software architecture.

This document provides a detailed technical description for robotics engineers deploying ergoCub003. It covers hardware architecture, electromechanical design specifics (particularly the neck, wrist, and hand subsystems), sensorimotor configuration, embedded board organization, and the dual-computer operating system architecture.

---

## Hardware Overview

ergoCub-S/N:003 is a full-body humanoid platform with a modular electromechanical design optimized for force control and physical interaction. The platform comprises six primary articulated subsystems plus an integrated sensing suite.
More information about the hardware and robot logic can be found at: https://github.com/mesh-iit/electronics-wiring-public/tree/master/ergocub1/ergocub1.4/pdf .

### Main Body Structure

- **Head**: 4-DOF neck articulation with camera pan-tilt control, mounted on a redesigned Neck [MK3 mechanism](https://mesh-iit.github.io/documentation/necks/neck_mk3/)
- **Torso**: 3-DOF waist (roll-pitch-yaw) providing trunk flexibility
- **Left Arm**: 13-DOF limb including 3-DOF spherical wrist ([MK2.1 design](https://mesh-iit.github.io/documentation/wrists/wrist_mk2/)) and 12-DOF hand ([MK5.3](https://mesh-iit.github.io/documentation/hands/hands_mk5/) with precision finger actuation)
- **Right Arm**: 13-DOF limb mirroring left arm configuration
- **Left Leg**: 6-DOF lower limb for locomotion (hip, knee, ankle)
- **Right Leg**: 6-DOF lower limb for locomotion (hip, knee, ankle)


### Mechanical Transmission

All actuators employ **direct-drive or geared motor systems** with integrated encoders for joint state feedback. The design emphasis is on transparent force control and impedance modulation, achieved through:
- Low-inertia actuators selected for each joint functional role
- Hard endpoint stops for collision safety
- Distributed force/torque sensing at critical manipulation and locomotion points
- Elastic joint limits on critical hand and wrist joints

---

## Motors and Sensors

### Neck Subsystem (MK3)

The **Neck MK3** mechanism is a modern tendonless design with a serial kinematic configuration. It features three primary rotation axes ordered bottom-to-top as:
1. **Pitch** (forward/backward head inclination)
2. **Roll** (side-to-side head tilt)
3. **Yaw** (head rotation about vertical axis)

This ordering provides intuitive control of gaze direction and head orientation, with the yaw axis topmost for minimal inertia effects on the pitch and roll servos.
For more information about the Neck MK3, check the [documentation](https://mesh-iit.github.io/documentation/necks/neck_mk3/).


### Wrist Subsystem (MK2.1)

The forearm-to-hand connection in ergoCub employs the **Wrist MK2.1 mechanism**, a spherical joint design enabling three degrees of rotational freedom in a compact, backdrivable structure. The wrist translates three motor commands into coordinated roll-pitch-yaw motions of the hand with respect to the forearm.

#### Kinematic Structure


The Wrist MK2 consists of three rotational joints in series, producing a spherical wrist with workspace oriented around the hand palm:

| Joint | Mechanical Role | Description |
|-------|-----------------|-------------|
| **Wrist Yaw** (W1) | Primary azimuth | Rotation about forearm longitudinal axis; defines hand twist |
| **Wrist Roll** (W2) | Intermediate rotation | Coordinated with yaw for intuitive hand orientation |
| **Wrist Pitch** (W3) | Vertical orientation | Flexion/extension of hand about lateral axis |

For more information about the Wrist MK2.1, check the [documentation](https://mesh-iit.github.io/documentation/wrists/wrist_mk2/).


### Hand Subsystem (MK5.3)

The ergoCub hands represent a sophisticated dexterous manipulation platform with 6 degrees of freedom per hand distributed across the five digits. The current ergoCub-S/N:003 systems are equipped with **Hand MK5.3**, which features expanded joint ranges compared to earlier MK5 variants.

For more information about the Hand MK5.3, check the [documentation](https://mesh-iit.github.io/documentation/hands/hands_mk5/#mk53).

---

## Sensory Systems

### Force/Torque (F/T) Sensors

For more detailed information, check the [documentation](https://mesh-iit.github.io/documentation/ft_sensors/).
Additional information about the F/T sensor client interface is available at: https://mesh-iit.github.io/documentation/robot_sensors/yarp_nws_convention/?h=IMU#force-torque-sensors.

**Purpose**: Monitor contact forces and joint torques for force control and manipulation.

**Design Philosophy**: ergoCub uses 6-axis F/T sensors strategically placed at manipulation and locomotion points to enable **force-controlled interactions** with the environment. This is a key distinction from iCub, where F/T feedback is primarily used for passive impedance estimation.

**Note**: ergoCub's F/T sensors are inherently **low-noise** designs, making them suitable for closed-loop force control (unlike velocity or acceleration estimation). They provide 6-axis force/torque measurement. They should be prioritized in any safety-critical interaction framework.

- **Right/Left Arm**: 
  - Mounted on EB1 and EB2 (shoulder region)
  - Scope: Arm contact force monitoring, manipulation force feedback

- **Left/Right Leg**:
  - Mounted on EB8 and EB6 (Hip region)
  - Mounted on EB9 and EB7 (Ankle region)
  - Scope: Gait analysis, balance control, floor contact detection



### Motor Temperature Sensors

For more detailed information, check the [documentation](https://mesh-iit.github.io/documentation/temperature_sensors/).

**Purpose**: Monitor motor winding temperatures to prevent overheating and enable thermal-aware control strategies.

**Sensor Architecture**:
- **Physical Sensor**: PT100 or PT1000 resistance temperature detectors (RTDs) embedded in motor windings
- **Temperature Detection Board (TDB)**: Converts RTD resistance measurements to digital values via I2C protocol

For all joints the limits set are:
- Hardware Limit: 110°C
- Warning Limit: 90°C


**Reading Motor Temperature Data**:
1. **Custom Monitoring Module**: Recommended approach for thermal-aware control; see [motorStatePublisher](https://github.com/robotology/robots-configuration/tree/master/ergoCubSN003/extra/motorStatePublisher) reference implementation


**Safety Notes**:
- Temperature-constrained motors have different current limits (see commented values in motor control files)
- Ankle roll motor is particularly sensitive to overheating; guidance is available in configuration files
- Automatic HW Fault triggers after 10 seconds above hardware limit; does not provide graceful derating

---

#### Inertial Measurement Units (IMUs)

For more detailed information, check the [documentation](https://mesh-iit.github.io/documentation/ft_sensors/ft_onboard_imu/).
Specific information about related kinematics is available at: https://mesh-iit.github.io/documentation/icub_kinematics/icub-forward-kinematics/icub-forward-kinematics-imu/. Additional details about the IMU client interface are at: https://mesh-iit.github.io/documentation/robot_sensors/yarp_nws_convention/?h=IMU#imu-client-device

**Purpose**: Provide orientation and acceleration feedback for proprioception, balance estimation, and external contact detection.

**Head IMU** (mounted on EB20, BNO055 6-axis sensor):
- **Measurement**: 3-axis acceleration + 3-axis angular velocity + integrated orientation (quaternion)
- **Applications**:
  - Visual gaze stabilization (eye reflex coordination)
  - Head collision detection (rapid acceleration spikes)
  - Orientation feedback for camera calibration
  - Integration with head F/T for impact force estimation

**Waist IMU** (mounted on torso structure, XSense MTi-600 9-axis sensor):
- **Measurement**: 3-axis acceleration + 3-axis angular velocity + 3-axis magnetic field
- **Applications**:
  - Whole-body Center-of-Mass (CoM) estimation when fused with leg F/T sensors
  - Torso sway detection during manipulation
  - Ground truth orientation for balance feedback
  - Integration with leg force sensors for dynamic walking control

---

#### External Sensors (Head-Mounted)

The ergoCub head integrates two primary exteroceptive sensors for scene understanding, navigation, and manipulation. Both sensors are mounted on the head and benefit from the Neck MK3's broad pitch range for environmental scanning:

- **RealSense D450 RGB-D Camera**

- **RPLidar S2 2D Laser Scanner**

In order to **enable the LiDAR data streaming on a ROS topic** you need to add a `_nws_ros2` wrapper in the configuration files as follows:

1. add the file `{robot-configuration-file}/wrappers/sensors/rplidar_wrapper_ros2.xml`

the file should have the following content:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE robot PUBLIC "-//YARP//DTD yarprobotinterface 3.0//EN" "http://www.yarp.it/DTD/yarprobotinterfaceV3.0.dtd">

<device xmlns:xi="http://www.w3.org/2001/XInclude" name="lidarWrapR" type="rangefinder2D_nws_ros2">
    <param name="period"> 0.1 </param>
    <param name="node_name"> rangefinder_ros2_node </param>
    <param name="topic_name"> /scan </param>
    <param name="frame_id">  lasersensor </param>
    <action phase="startup" level="10" type="attach">
        <paramlist name="networks">
        <elem name="the_device"> rpLidarS2 </elem>
        </paramlist>
    </action>
    <action phase="shutdown" level="15" type="detach" />
</device>
```

2. once that is done the configuration file needs to be added to the main configuration file for the lidar, similarly to how done here:

```xml
<!-- LIDAR -->
<xi:include href="hardware/sensors/rplidar.xml"/>
<xi:include href="wrappers/sensors/rplidar_wrapper_ros2.xml"/> 
```

Regarding the first xml file shown, it basically uses the `rangefinder2D_nws_ros2` device to configure a `ROS` topic called `/scan` that streams the data taken from the virtualized lidar device configured in the file `hardware/sensors/rplidar.xml`, that in this case is named `rpLidarS2`.

3. Applications for these sensors can be launched using yarpmanager.

---

## Power Distribution and Battery System

ergoCub-S/N:003 is designed for **autonomous operation** with an integrated battery pack and Battery Management System (BMS), distinguishing it from tethered or grid-powered research platforms.

This section provides general information about the power supply and battery system. More detailed information can be found at:

- BAT board: https://mesh-iit.github.io/documentation/battery_boards/bat_board/bat_board/
- BMS board: https://mesh-iit.github.io/documentation/battery_boards/bms_board/bms_board/
- ErgoCub battery pack: https://mesh-iit.github.io/documentation/ergocub_battery_pack/ergocub_battery_pack/


### Battery Management System (BMS)

The battery pack integrates a **dedicated BMS controller** (model: BMS_IIT1A-11S-50APK_PCA) which is **physically inseparable** from the pack.


#### Charging Procedure

ergoCub-S/N:003 is charged using a **dedicated charging station** with automated charge profiling:

1. **Insertion**: Place battery pack into designated charging slot
2. **Initialization**: Charger performs self-test and BMS communication validation
3. **Charging Phase**: Multi-stage (CC/CV) charging profile automatically selected based on battery state
4. **Completion**: Charger terminates automatically when battery reaches full charge (41.5-42.0 V nominal)
5. **Removal**: Battery may be removed once charging LED indicates completion

---

## Calibration System

All motors on ergoCub-S/N:003 require calibration after startup or power-down.  For more detailed information about the calibration types available, check: https://mesh-iit.github.io/documentation/robot_calibration_types/standard_calibration_types
It is important to keep the calibration order to avoid self collisions. If a joint could not calibrate, please pay attention to the collisions and if necessary press the fault button.


### Calibration Types used on ergoCub

#### Type 12: Analog Sensor Calibration
- Uses absolute position encoder for joint position
- Used on: wrist, head, finger abduction

#### Type 10: Hard Limit Calibration (Most Common)
- Uses hardware hard stops for calibration
- Position reference from relative encoder count
- Used on: Most arm, leg, and torso joints

#### Type 14: Analog Sensor Plus Hardware Limit Calibration
- Uses absolute position encoder for joint position  
- Uses the incremental encoder at the motor
- Used on: Hand Open-Close manipulation joints



#### Head Calibration

 - **Component**: Head (HeadV3_Calibrator)
 - **Total Joints**: 4
 - **Calibration Order**: Sequential (1) → (2) → (0) → (3)



#### Torso Calibration

 - **Component**: Torso (Torso_Calibrator)
 - **Total Joints**: 3
 - **Calibration Order**: Parallel (0, 1, 2)


#### Left Arm Calibration

 - **Component**: Left Arm (Left_Arm_Calibrator)
 - **Total Joints**: 13
 - **Calibration Order**: (4 5 6) → (3) → (2) → (0) → (1) → (7 8) → (9) → (10 11 12)


#### Right Arm Calibration

 - **Component**: Right Arm (Right_Arm_Calibrator)
 - **Total Joints**: 13
 - **Similar structure to left arm with mirrored calibration**


#### Left Leg Calibration

 - **Component**: Left Leg (Left_Leg_Calibrator)
 - **Total Joints**: 6
 - **Calibration Order**: (2) → (4) → (5) → (3) → (0) → (1)


#### Right Leg Calibration

 - **Component**: Right Leg (Right_Leg_Calibrator)
 - **Total Joints**: 6
 - **Calibration Order**: (4) → (5) → (2) → (3) → (0) → (1)

---

## Operating Systems Architecture

ergoCub-S/N:003 employs a **distributed dual-computer architecture** reflecting differences between sensing/perception (head) and motor control (torso). This design philosophy enables:
- Independent OS optimization for each control domain
- Scalable sensor processing without impacting real-time motor control
- Flexible deployment and updates without full system downtime

### System Topology

The ergoCub control architecture comprises two primary compute nodes networked via **10 Gbps Ethernet**.

#### ergocub-head (NVIDIA Jetson Xavier AGX)
- **Hardware**: NVIDIA Jetson Xavier AGX module with integrated GPU
- **Role**: Perception, vision processing, sensor data fusion
  
#### ergocub-torso (COM Express Type 10 Module)

- **Hardware**: Advantech COM Express Type 10 carrier board with industrial-grade embedded processor
- **Role**: Real-time motor control, force/torque sensing, balance

### Network Interfaces and Configuration

ergoCub operates on a **three-tier network architecture** connecting the head, torso, motor control boards, and external infrastructure. Understanding and properly configuring these networks is critical for robot operation and debugging.

More detailed information about setting up the robot network can be found at: https://mesh-iit.github.io/documentation/ergocub_operating_systems/network/ and its specific subsections:

- ergoCub-head: https://mesh-iit.github.io/documentation/ergocub_operating_systems/ergocub_head/
- ergoCub-torso: https://mesh-iit.github.io/documentation/ergocub_operating_systems/ergocub_torso/install_from_scratch/

#### Network Architecture Overview

The ergoCub network is divided into three independent subnets:

1. **Internal Network (10.0.1.0/24)**: Segregated motor control network
   - Connects ergocub-torso to all motor control boards (EB1-EB31)
   - No external connectivity (isolated for reliability and real-time performance)
   - Static configuration managed by motor board firmware

2. **External Network (10.0.2.0/24)**: Primary communication and internet access
   - Connects ergocub-torso and ergocub-head to the ergocub-server
   - Supports internet connectivity via WiFi or wired uplink
   - Enables remote monitoring, software updates, and sensor streaming

3. **Backup Network (10.0.0.0/24)**: Direct troubleshooting and recovery
   - Direct Ethernet link between ergocub-torso and ergocub-head
   - Used for emergency intervention when external network fails
   - Enables direct debugging without server dependency

#### Physical Ethernet Interfaces

**ergocub-torso**:
- **eth0**: Internal network interface (10.0.1.x subnet) — **connected to motor boards via internal switch**
- **eth1**: Backup network interface (10.0.0.x subnet) — **direct Ethernet cable to ergocub-head**
- **WiFi (wlan0)**: External network interface (10.0.2.x subnet) — **wireless link to ergocub-server**

**ergocub-head**:
- **eth0 + eth1 (bridged)**: Backup network interface (10.0.0.x subnet) — **receives connectivity from ergocub-torso**
- **WiFi (wlan0)**: External network interface (10.0.2.x subnet) — **wireless link to ergocub-server**

#### Internal Network (10.0.1.0/24) - Motor Control

**Purpose**: Direct Ethernet communication with embedded motor control boards (EB1-EB31)

**Fixed Configuration** (firmware-determined, not user-configurable):

| Parameter | Value |
|-----------|-------|
| **Subnet** | 10.0.1.0/24 |
| **ergocub-torso IP** | 10.0.1.104 (static) |
| **Netmask** | 255.255.255.0 |
| **Default Gateway** | None (isolated network) |
| **Board IP Range** | 10.0.1.1 - 10.0.1.31 (EB1-EB31 mapped 1:1) |
| **Update Rate** | Continuous (1 KHz motor control loop) |

**Troubleshooting**:
- If eth0 has no IP address, the internal Ethernet interface may be down
- Check physical Ethernet cable connection to internal motor board switch
- Verify motor board firmware is up-to-date (boards auto-configure 10.0.1.x addresses)
- If specific boards are unreachable, check individual board power and CAN bus connections

#### External Network (10.0.2.0/24) - Server and Internet

**Purpose**: Connect ergocub-head and ergocub-torso to ergocub-server and internet infrastructure

**Default Configuration** (recommended static setup):

| Parameter | ergocub-torso | ergocub-head |
|-----------|---|---|
| **Subnet** | 10.0.2.0/24 | 10.0.2.0/24 |
| **IPv4 Address** | 10.0.2.2 (static) | 10.0.2.3 (static) |
| **Netmask** | 255.255.255.0 | 255.255.255.0 |
| **Default Gateway** | 10.0.2.1 | 10.0.2.1 |
| **DNS Server(s)** | 10.0.2.1, 8.8.8.8 | 10.0.2.1, 8.8.8.8 |
| **Interface** | WiFi (wlan0) | WiFi (wlan0) |

---

### Network Communication (High-Level Overview)

The two computers communicate over the robot's **internal Ethernet backbone**:

| Parameter | Specification |
|-----------|---|
| **Primary Interface** | WiFi on external network (10.0.2.0/24) for ROS2 and YARP |
| **Motor Control** | Internal network eth0 (10.0.1.0/24) for EB board communication |
| **Emergency Fallback** | Backup network eth1 (10.0.0.0/24) for direct troubleshooting |
| **Typical Bandwidth** | ~50-100 Mbps sustained on external network (depending on vision FPS) |
| **Control Latency** | <20 ms typical (motor command → response via internal network) |
| **NTP Sync** | Coordinated via ergocub-server (10.0.2.1) at 1-5 second intervals |


### Swap ETH cabled and WiFi Network

In order to enabling the WiFi network on `ergocub` you first need to check that the WiFi network interface is activated on `ergocub-head` and you can follow 2 different ways:

- an easy way is to just connect the `ergocub-head` board to an available WiFi network using the following commands:

```bash
ssh ergocub-head -X
sudo mntui
```
at this point from the UI that gets opened you just need to select the desired network and activate it

- the other option is to create a new static IP network (in this case it is recommended to use an IP address that is different from the one of the cabled network, i.e. 10.0.1/24). Similarly to what done in the first option you need to access the network UI:

```bash
ssh ergocub-head -X
sudo mntui
```

Once here, you need to use the edit option and create the desired network.

After doing that you can edit the following files depending on the desired network you wish to attach to:

- update the `/etc/hosts` file with either wireless or ETH IP for the `ergocub-torso`, `ergocub-head` and `ergocub-laptop`
- update the [yarp conf](https://www.yarp.it/latest/group__yarp.html#yarp_conf) on the same machines, i.e. `ergocub-torso`, `ergocub-head` and `ergocub-laptop`

It is important to notice that the network interface mounted on `ergocub-head` board does not support wpa and wpa2 enterprise security. 

### SSH passwordless login

This configuration is mandatory for the correct startup of `yarpdev` managed by the `yarpmanager`.
To complete its configuration just few steps are needed as follows:

1. `ssh-keygen` Note: This is used just the first time; there is no need to use it again since the key is already generated
2. `ssh-copy-id ergocub@ergocub-torso` (as an alternative also **ergocub@ip-address-ergocub-torso**)
3. `ssh-copy-id ergocub@ergocub-head` (as an alternative also **ergocub@ip-address-ergocub-head**)
4. `ssh-copy-id ergocub@ergocub-laptop` (as an alternative also **ergocub@ip-address-ergocub-laptop**)

!!! note
    This configuration is necessary only on the node where yarpmanager will be executed.
    In most use cases `yarpmanager` application are run on all nodes, thus we complete all the steps above.



### Operating System Choices

#### ergocub-head: Ubuntu + NVIDIA Jetpack

**OS Configuration**:
- **Base OS**: Ubuntu 22.04
- **Jetpack Version**: NVIDIA Jetpack 6.x (CUDA 12.x available)
- **CUDA Support**: Full CUDA Toolkit with cuDNN, cuBLAS for GPU-accelerated vision
- **Middleware**: ROS2 Humble/Iron with geometry_msgs, sensor_msgs, vision_msgs packages

**Post-Flashing Requirements**:
1. Install CUDA libraries and development tools
2. Install librealsense SDK for RealSense camera support
3. Install jtop for monitoring (GPU memory, thermal limits)
4. Setup ergoCub OLED display driver and initialization scripts
5. Configure camera calibration files and auto-exposure parameters

**Typical Software Stack**:
- OpenCV 4.x for image processing
- Depth registration and point cloud generation (librealsense or OpenCV)
- YOLO/TensorRT for real-time object detection
- ROS2 nodes for sensor publishing (camera_info, depth_to_laserscan bridge)

#### ergocub-torso: Ubuntu Server with Real-Time Extensions

**OS Configuration**:
- **Base OS**: Ubuntu 24.04 LTS Server
- **Kernel**: Linux kernel with real-time patches (PREEMPT_RT) for deterministic control
- **Network Time Protocol**: NTP synchronization via local network (10.0.2.1) or ntp.ubuntu.com
- **Middleware**: YARP with optimized Ethernet communication drivers

**Manual Installation Process**:
1. Install Ubuntu 24.04 Server from bootable media
2. Configure static IP address for robot network integration
3. Configure NTP for time synchronization (editing `/etc/default/ntpdate`)
4. Install YARP and robotology-superbuild dependency stack
5. Deploy motor control firmware to embedded boards (EB1-EB31)
6. Validate Ethernet connectivity to all boards

**System Hardening**:
- Disable unnecessary services (DHCP client, IPv6, unused protocols)
- Configure read-only filesystem for permanent configurations
- Enable watchdog timers for safety (automatic restart on control loop timeout)
- Configure UPS/battery integration for graceful shutdown on power loss

### Firmware Updates and Reflashing

#### ergocub-head Reflashing
1. Obtain NVIDIA Jetpack image (.tar or .img file)
2. Use NVIDIA SDK Manager or `dd` utility to write to eMMC
3. Boot into recovery mode (FORCE_RECOVERY button)
4. Flash and wait for Jetpack installation (~30-40 minutes)
5. Post-flash: install CUDA, librealsense, jtop, ergoCub display driver

#### ergocub-torso Reflashing
1. Boot Ubuntu 24.04 Server installer from USB
2. Partition disk with /boot, /, and optional /var partitions
3. Post-install: configure NTP, install YARP, deploy superbuild
4. Flash embedded board firmware via firmwareupdater.ini configuration
5. Validate all EB (embedded board) Ethernet responses

#### Embedded board Reflashing
it is possible to update the firmware of each embedded board following [this documentation](https://mesh-iit.github.io/documentation/icub_firmware/firmware/firmware/?h=firmware#firmwareupdater).

### Storage and Filesystem

| Drive | OS | Capacity | Use |
|-------|----|----|---|
| **ergocub-head** | eMMC | 32 GB | System + vision datasets |
| **ergocub-torso** | SSD or eMMC | 256 GB+ | System + motor logs + calibration data |

Both systems maintain local sensor logs in `/var/log/robot/` for troubleshooting and system diagnostics.

---

## Software and Applications

The ergoCub runs on YARP middleware with a comprehensive software stack for robot interface, control, and monitoring. Applications can be launched via YARP robot interface or yarpmanager.

### Core System Interface

**yarprobotinterface**
- Primary interface for hardware initialization and configuration
- Loads all device drivers and wrappers
- Main configuration: `ergocub_all.xml`
- Per-component configurations: `head.xml`, `torso.xml`, `left_arm.xml`, etc.
- Manages startup/shutdown sequences with priority levels
- Handles calibration triggers and data streams

---

### Motor Control Applications

**yarpmotorgui** (Motor Control GUI)
- Interactive graphical interface for joint control
- Real-time position, velocity, and torque visualization
- Available body parts: head, torso, left_arm, right_arm, left_leg, right_leg
- Usage: `yarpmotorgui --robot ergocub --parts "(head torso left_arm right_arm left_leg right_leg)"`
- Features:
  - Individual joint sliders for precise control
  - Current monitoring
  - Temperature readouts
  - Emergency stop capabilities


### [Yarp Manager](https://www.yarp.it/latest/group__yarpmanager.html)
Is a tool for running and managing multiple programs on a set of machines.
---

### Sensor Data Publishing

**motorTemperaturePublisher** 
- Publishes motor temperatures by body part (not available for head and lower arm)
- Configuration per body part:
  - `config_left_leg.ini`
  - `config_right_leg.ini`
  - `config_torso.ini`
- Generates temperature plots via:
  - `plotTemperatureLeftLeg.xml`
  - `plotTemperatureRightLeg.xml`
  - `plotTemperatureTorso.xml`
- Use case: Thermal monitoring, motor health assessment

---

### Firmware Management

More detailed information can be found at: https://mesh-iit.github.io/documentation/icub_firmware/firmware/firmware/

---

### Starting the robot

The ergoCub robot control system can be started through a sequence of commands executed on `ergocub-torso`, or alternatively through the graphical application launcher on `ergocub-laptop`.

#### Method 1: Command Line Startup (ergocub-torso)

1. **Connect to ergocub-torso via SSH**:
   ```bash
   ssh ergocub@ergocub-torso
   ```

2. **Navigate to robot configuration directory** using the alias:
   ```bash
   gotorobotsconfiguration
   ```
   This alias brings you to the ergoCub configuration directory where all robot control files are located.

3. **Initialize hardware and calibration** by running:
   ```bash
   yarprobotinterface
   ```
   This command:
   - Performs hardware initialization
   - Loads motor control drivers for all joints
   - Executes calibration routines
   - Establishes YARP middleware connections

4. **Open the motor control GUI** by running from the same directory:
   ```bash
   yarpmotorgui
   ```
   This launches the interactive motor control interface displaying:
   - All robot body parts (head, torso, left_arm, right_arm, left_leg, right_leg)
   - Individual joint controls with sliders for position adjustment
   - Real-time feedback for position, velocity, and current
   - The active control mode

#### Method 2: Graphical Application Launcher (ergocub-laptop)

Alternatively, the same startup sequence can be executed automatically from `ergocub-laptop` using **yarpmanager**:

1. Launch yarpmanager from ergocub-laptop
2. Run 'yarpserver' and the 'yarprun' on the single node of the network
3. Select the **ergoCubStartup** application
4. Run the application to automatically execute:
   - yarplogger initialization
   - yarprobotinterface (hardware initialization & calibration)
   - yarpmotorgui (motor control interface)

This graphical method provides an alternative to manual command-line startup and is useful for monitoring the startup process.

---

## Additional System Information


### Start yarprobotinterface with one or more parts disabled
 Here you can find the detailed documentation: https://www.yarp.it/git-master/group__yarp__robotinterface__xml__config__files.html


### Telemetry System

https://robotology.github.io/robometry/classrobometry_1_1TelemetryDeviceDumper.html

- `telemetryDeviceExternal.xml` - External telemetry streaming
- Enables remote monitoring of robot state
- Exports file .mat for a data analysis

---

## Troubleshooting

This section addresses the most common operational issues and recovery procedures for ergoCub.

### Resolving HW Fault on a Joint

**Symptoms**: A specific joint stops responding or displays a hardware fault warning in yarpmotorgui.

**Common Causes**:
- Motor overheating (temperature exceeded warning or hardware limit)
- Calibration drift or loss of position reference
- CAN bus communication error with embedded board
- Mechanical jamming or collision



## Recovery Steps

- Check the `yarprobotinterface` log using `yarplogger`. The log usually contains information about the cause of the fault.
- Verify the physical integrity of the joint and ensure that it can move freely without mechanical obstruction.

**IMPORTANT:**  
It is essential to identify and resolve the root cause of the fault before proceeding (for example, an overcurrent condition).

- If the issue occurs **after calibration**, disable and then re-enable the joint using `yarpmotorgui`. In most cases this resolves the problem.

- If the issue occurs **during or before calibration**, try the following:
  1. Shut down all applications.
  2. Power off the motors.
  3. Restart the system and run the applications again.

- If you suspect **CAN communication issues**, check the CAN connection using `FirmwareUpdater`.

If the problem cannot be resolved, open a ticket and include the **complete `yarprobotinterface` log**.  
Providing the full log helps us identify and diagnose the cause of the fault.

---

### Faulting the Robot

**Definition**: Complete motor halt and system safety shutdown

**When to Use**:
- Emergency situation requiring immediate cessation of all motion
- Safety hazard detected in the environment
- System malfunction or control loss

**Implementation**:
- Emergency stop button available in `yarpmotorgui` interface
- Command-line stop via YARP port addressing
- Full power cycle as last resort

---

### Checking That the Walking Module is Running

**Verification Steps**:
- Query YARP network ports for walking module presence
- Monitor balance feedback from waist and leg F/T sensors
- Verify leg joint commands are being received and tracked
- Check locomotion feedback in system logs

**Expected Behavior**:
- Coordinated hip, knee, and ankle joint trajectories
- Consistent F/T sensor readings during stance phase
- Smooth torso orientation maintained via waist IMU feedback

---

### Recover the Robot from Undesired Condition While Walking Module Has Started

**Symptoms**: Robot enters unstable state, loses balance, or exhibits unexpected movement during walking.

**Emergency Recovery**:
- Activate emergency stop immediately
- Wait for all joints to halt completely
- Manually support robot if balance is compromised
- Disable walking module via yarpmanager or command line
- Restart walking module after system stabilization

**Post-Recovery**:
- Verify leg joint calibration is intact
- Check F/T sensor readings are within normal range
- Review system logs for fault indicators
- Re-initialize walking module with safe initial conditions

---

### Battery Pack Hot Swap

**Procedure**:
1. Ensure robot is in safe stationary configuration
2. Place ergoCub in secure support (wall mount or handling frame)
3. Power down robot gracefully (request shutdown via BMS or emergency stop)
4. Wait for all active indicators to extinguish (~30 seconds)
5. Remove depleted battery pack from charging slot
6. Insert fully charged battery pack into slot
7. Verify battery indicator LED signals correct insertion
8. Re-power robot and verify all systems initialize normally

**Battery Status Monitoring**:
- Check battery voltage and charge state via BMS board readouts
- Monitor battery temperature using integrated thermal sensors
- Ensure charger confirms full charge before hot swap operation (LED indicator)

**Safety Notes**:
- Never hot-swap while robot is powered on or calibrating
- Ensure battery pack is fully inserted to establish power connections
- Allow 5-minute stabilization period before resuming normal operation after swap
- BMS will auto-disconnect if battery is removed improperly during operation

---

*Document Version: 1.0*  
*Last Updated: March 2026*  
*Robot Platform: ergoCub-S/N:003*
