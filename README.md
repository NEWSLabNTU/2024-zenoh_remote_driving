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
make build
```

# Run This Project

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
