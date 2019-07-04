FROM java:8

# Versions of different tools installed.
ENV NODEJS_VERSION="v8.9.3"
ENV BAZEL_VERSION="0.8.0"
ENV ANDROID_TOOLS_VERSION="3859397"

RUN echo "deb [check-valid-until=no] http://cdn-fastly.deb.debian.org/debian jessie main" > /etc/apt/sources.list.d/jessie.list
RUN echo "deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list
RUN sed -i '/deb http:\/\/deb.debian.org\/debian jessie-updates main/d' /etc/apt/sources.list
RUN apt-get -o Acquire::Check-Valid-Until=false update

RUN apt-get install -y \
      sox \
      curl \
      libicu-dev \
      g++ \
      git \
      python \
      python-dev \
      python-setuptools \
      python3 \
      python3-dev \
      python3-setuptools \
      python3-pip \
      unzip \
      wget \
      nano

# Clone language resources
WORKDIR /usr/local/src
RUN git clone https://github.com/google/language-resources

# Load language resources python modules
ENV PYTHONPATH="/usr/local/src/language-resources"

# Install python pip
WORKDIR /opt
RUN curl -k https://bootstrap.pypa.io/get-pip.py > get-pip.py && ls -l && python get-pip.py && rm get-pip.py
RUN pip install PyICU
#RUN pip3 install PyICU flask

# Install android SDK
#RUN wget https://dl.google.com/android/repository/sdk-tools-linux-${ANDROID_TOOLS_VERSION}.zip  \
#      && mkdir -p -m 1777 /usr/local/android-sdk  \
#      && unzip sdk-tools-linux-${ANDROID_TOOLS_VERSION}.zip -d /usr/local/android-sdk  \
#      && echo y | /usr/local/android-sdk/tools/bin/sdkmanager 'build-tools;26.0.3' 'platforms;android-24' \
#      && rm sdk-tools-linux-${ANDROID_TOOLS_VERSION}.zip

# Install bazel
RUN wget https://github.com/bazelbuild/bazel/releases/download/${BAZEL_VERSION}/bazel-${BAZEL_VERSION}-installer-linux-x86_64.sh \
      && bash bazel-${BAZEL_VERSION}-installer-linux-x86_64.sh --user \
      && rm bazel-${BAZEL_VERSION}-installer-linux-x86_64.sh

# Add bazel to path
ENV PATH=/root/bin:$PATH

# Install Nodejs
WORKDIR /opt/
#RUN wget http://storage.googleapis.com/gae_node_packages/node-${NODEJS_VERSION}-linux-x64.tar.gz \
#      && tar -xf node-${NODEJS_VERSION}-linux-x64.tar.gz \
#      && rm node-${NODEJS_VERSION}-linux-x64.tar.gz

#ENV PATH $PATH:/opt/node-${NODEJS_VERSION}-linux-x64/bin

# Set common env vars
#ENV NODE_ENV production

RUN  apt-get install -y \
      automake \
      bc \
      curl \
      g++ \
      git \
      libc-dev \
      libreadline-dev \
      libtool \
      make \
      ncurses-dev \
      nvi \
      pkg-config \
      wavpack \
      zip \
      zlib1g-dev \
      net-tools
# Fetch and prepare Festival & friends
WORKDIR /usr/local/src/tools
ENV FESTIVAL_SUIT_PATH /usr/local/src/tools
COPY setup_festival.sh /usr/local/src/tools/setup_festival.sh
RUN /usr/local/src/tools/setup_festival.sh

RUN rm /usr/local/src/tools/festival/lib/festival.el

# Set env variables
ENV ESTDIR /usr/local/src/tools/speech_tools
ENV FESTVOXDIR /usr/local/src/tools/festvox
ENV FESTIVALDIR /usr/local/src/tools/festival
ENV FLITEDIR /usr/local/src/tools/flite
ENV SPTKDIR /usr/local/src/tools/
ENV EXDIR /usr/local/src/tools/examples

# Add festival to path
ENV PATH="/usr/local/src/tools/festival/bin:${PATH}"

WORKDIR /usr/local/src/

# setup TTS
COPY make5.zip /usr/local/src/
RUN unzip make5.zip
RUN rm make5.zip
ENV OUTPUT_VOICE_FOLDER /usr/local/src/tts2
WORKDIR /usr/local/src/tts2

RUN pip3 install flask
COPY app.py /usr/local/src/tts2
RUN ifconfig
#ENTRYPOINT ["python3"]
RUN chmod -x app.py
ENV FLASK_APP /usr/local/src/tts2/app.py
CMD ["python3","-m","flask","run","--host=0.0.0.0"]