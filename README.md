# zenoh_remote_driving
It's the project for the purpose of deploying the remote driving task over Zenon


# Prerequisites

- ROS2
- Python 3.8
- RUST >= 1.76.0

- Testing Environment :
    - Operator : Ubuntu 20.04
    - Vehicle : F1EIGHTH (with Ubuntu 22.04)


# Build Dependency

```bash=
cd zenoh_remote_driving/
git submodule update --init --recursive
cd external/zenoh-plugin-ros2dds
cargo build --release
```


# Build Project

```bash=
cd zenoh_remote_driving
make build_project
make build_proxy
```

# Run

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
