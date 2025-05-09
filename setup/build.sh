#!/bin/bash

version=$(cat ./version)
v1=$(echo $version| awk -F . '{print($1)}')
v2=$(echo $version| awk -F . '{print($2)}')
v3=$(echo $version| awk -F . '{print($2)}')
_v3=$(expr $v3+1)
new_version="$v1.$v2.$v3"
image="spider:$new_version"

docker build -f DockerFile -t $image .


