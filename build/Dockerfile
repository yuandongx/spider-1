FROM dong01/app-base:v0.1

ENV  APP_DTA_DIR=/home/openeuler/workspace/spider-1/data APP_MONGO_HOST=123.249.37.220 VERSION=1.0.0

# Install system dependencies
COPY . /app
RUN pip config --user set global.index https://mirrors.huaweicloud.com/repository/pypi;\
    pip config --user set global.index-url https://mirrors.huaweicloud.com/repository/pypi/simple;\
    pip config --user set global.trusted-host mirrors.huaweicloud.com;\
    pip install --no-cache-dir --upgrade pip;\
    pip install --no-cache-dir -r /app/requirements.txt;

# Set the working directory
WORKDIR /app
CMD ["/bin/bash", "./build/start.sh"]