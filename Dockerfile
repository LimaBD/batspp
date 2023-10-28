# This builds the base images that we can use for development
#
# Build the image:
# $ docker build --no-cache --build-arg UBUNTU_VERSION=latest --build-arg PYTHON_VERSION=3.9.18 -t batspp-dev -f- . <Dockerfile
#
# Run the image:
# $ docker run -it --rm --mount type=bind,source="$(pwd)",target=/home/batspp batspp-dev
#
# Run the tests:
# $ docker run --entrypoint './tools/run_tests.bash' -it --rm --mount type=bind,source="$(pwd)",target=/home/batspp batspp-dev
#

ARG UBUNTU_VERSION
FROM ubuntu:${UBUNTU_VERSION}

ARG WORKDIR=/home/batspp
WORKDIR $WORKDIR

ENV DEBIAN_FRONTEND=noninteractive

# Install Git, wget and other dependencies.
RUN \
  apt-get update && apt-get install -y \
  git \
  wget && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Compile python from source, this avoid unsupported
# library problems but increase time to build
ARG PYTHON_VERSION
RUN apt update -y && apt upgrade -y \
    && apt-get install -y wget build-essential checkinstall libncursesw5-dev  libssl-dev  libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev && \
    cd /usr/src && \
    wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar xzf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations && \
    make install

# Some tools expect a "python" binary.
RUN ln -s $(which python3) /usr/local/bin/python

# Set the working directory visible.
ENV PYTHONPATH="${PYTHONPATH}:$WORKDIR"

# Install bsdmainutils for the
# Hexdump tool used for debugging
RUN apt-get update -y && \
  apt-get install -y bsdmainutils

# Also install sudo required for some usage
# cases as writing files, etc
RUN apt install sudo

# Install bats-core
RUN \
  GIT_SSL_NO_VERIFY=1 git clone https://github.com/bats-core/bats-core.git \
  && cd bats-core \
  && ./install.sh /usr/local

# Install the Python dependencies.
RUN sudo apt install python3-pip -y
RUN python -m pip install --upgrade pip
COPY ./requirements/development.txt $WORKDIR/requirements/development.txt
RUN python -m pip install -r $WORKDIR/requirements/development.txt
COPY ./requirements/production.txt $WORKDIR/requirements/production.txt
RUN python -m pip install -r $WORKDIR/requirements/production.txt
