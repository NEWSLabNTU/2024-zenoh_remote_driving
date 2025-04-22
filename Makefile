.PHONY: help build clean run_vehicle run_pilot

OPERATOR_IP = 192.168.225.71

help:
	@echo 'Usage:'
	@echo '    make help     Show this help message'
	@echo '    make build    Build the project'
	@echo '    make clean    Remove built artifacts'

prepare:
	pip install Adafruit-PCA9685==1.0.1
	rosdep install -y --from-paths src --ignore-src --rosdistro humble

build:
	colcon build \
		--symlink-install \
		--cmake-args -DCMAKE_BUILD_TYPE=Release

run_pilot:
	export ROS_DOMAIN_ID=6 && \
	. install/setup.sh && \
	gnome-terminal -- ros2 run autoware_manual_control keyboard_control && \
	ros2 launch rdrive_launch pilot.launch.yaml


run_vehicle:
	export ROS_DOMAIN_ID=9 && \
	. install/setup.sh && \
	ros2 launch rdrive_launch vehicle.launch.yaml operator_ip:=$(OPERATOR_IP)

clean:
	rm -rf build install log

# build_proxy:
# 	cd src/ffmpeg/ && g++ proxy.cpp -o proxy
