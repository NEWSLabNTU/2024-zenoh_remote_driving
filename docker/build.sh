#!/usr/bin/env bash
set -e
script_dir=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
cd "$script_dir"

usage() {
    echo "Usage: $0 [IMAGE_NAME]" >&2
    exit 1
}

default_image_name="autoware_remote_driving"
image_name="${1:-$default_image_name}"

docker build --platform=linux/arm64 -t "$image_name" .
echo "Built a Docker image: $image_name"
