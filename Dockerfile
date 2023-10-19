# This builds the base images that we can use for development
#
# Build the image:
# $ docker build --build-arg UBUNTU=latest --build-arg PYTHON=3 -t batspp-dev -f- . <Dockerfile
#
# Run the image:
# $ docker run -it --rm --mount type=bind,source="$(pwd)",target=/home/batspp batspp-dev
#
# Run the tests:
# $ docker run --entrypoint './tools/run_tests.bash' -it --rm --mount type=bind,source="$(pwd)",target=/home/batspp batspp-dev
#

ARG UBUNTU
FROM ubuntu:${UBUNTU}

ARG WORKDIR=/home/batspp
WORKDIR $WORKDIR

# Install python plus and python-venv so we can
# generate an isolated Python environment inside the container.
ARG PYTHON
RUN \
  apt-get update \
  && apt-get install -y --no-install-recommends \
  git \
  python${PYTHON} \
  wget && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Some tools expect a "python" binary.
RUN ln -s $(which python${PYTHON}) /usr/local/bin/python

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
