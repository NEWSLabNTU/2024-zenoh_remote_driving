.PHONY: help build clean

help:
	@echo 'Usage:'
	@echo '    make help     Show this help message'
	@echo '    make build    Build the project'
	@echo '    make clean    Remove built artifacts'

build:
	colcon build \
		--symlink-install \
		--cmake-args -DCMAKE_BUILD_TYPE=Release

clean:
	rm -rf build install log
# build_proxy:
# 	cd src/ffmpeg/ && g++ proxy.cpp -o proxy
