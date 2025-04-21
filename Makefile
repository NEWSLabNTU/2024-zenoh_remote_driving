.PHONY: help build clean run_vehicle run_pilot

help:
	@echo 'Usage:'
	@echo '    make help     Show this help message'
	@echo '    make build    Build the project'
	@echo '    make clean    Remove built artifacts'

prepare:
	rosdep install -y --from-paths src --ignore-src --rosdistro humble

build:
	colcon build \
		--symlink-install \
		--cmake-args -DCMAKE_BUILD_TYPE=Release

run_pilot:
	. install/setup.sh && \
	ros2 launch rdrive_launch pilot.launch.yaml

run_vehicle:
	. install/setup.sh && \
	ros2 launch rdrive_launch vehicle.launch.yaml

clean:
	rm -rf build install log
# build_proxy:
# 	cd src/ffmpeg/ && g++ proxy.cpp -o proxy
