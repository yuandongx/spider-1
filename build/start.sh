#!/bin/bash

# 后台启动redis
redis-server --daemonize yes

python main.py