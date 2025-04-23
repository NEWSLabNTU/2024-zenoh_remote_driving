# Remote Driving Demo
It's the project to deploy the remote driving task over Zenoh.


# Prerequisites

The project was tested on Jetpack 6.0 on a NVIDIA AGX Orin box.

- ROS Humble ([link](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html))
- Autoware 2025.02. It's recommended to install the Debian package
  released by NEWSLAB
  [here](https://github.com/NEWSLabNTU/autoware/releases/tag/rosdebian%2F2025.02-1).
- `zenoh-bridge-ros2dds`. You can install the Debian package [here](https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds?tab=readme-ov-file#linux-debian).
- Make sure the [F1EIGHTH](https://github.com/NEWSLabNTU/F1EIGHT.git)
  repo is already built in the **$HOME/repos** directory.

# Build This Project

```bash
source ~/repos/F1EIGHTH/install/setup.bash
make build
```

# Run This Project

## The New Way

We assumes the following IP assignments. Make sure your IP address is
correctly configured.

- Operator IP: 192.168.225.71
- Vehicle IP: 192.168.225.73

Source the setup scripts whenever you start a terminal on both vehicle
and pilot sides.

```bash
source ~/zenoh_remote_driving/install/setup.bash
```

### Step 1: Vehicle

To run with default settings,

```sh
make run_vehicle
```

Or to set the operator IP address to connect to,

```sh
make run_vehicle OPERATOR_IP=X.Y.Z.W
```

### Step 2: Operator

First, run the pilot system. It will prompt a RViz window. You can
wait a few seconds until the point cloud and video show up.

```sh
make run_pilot
```

### Step 3: Run Keyboard Controller

**Connect to the vehicle via SSH.** Open the keyboard controller.

```
ssh jetson@192.168.225.73
make controller
```

# Run This Project (Classical Way)

> [!NOTE]
> WARNING: The instructions are outdated here.

> [!NOTE]
> Before execution, the **VEHICLE_IP** and **OPERATOR_IP** variables in the **env.sh** must be manually configured.

- Vehicle

```bash=
source env.sh
cd zenoh_remote_driving
./src/ffmpeg/proxy

# Open another window to execute the following command.
source env.sh
bash ./script/vehicle.sh
```

- Operator

```bash=
cd zenoh_remote_driving
source env.sh
bash ./script/operator.sh
```
