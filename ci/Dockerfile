FROM debian:10-slim

RUN apt-get update && apt-get install -y \
  imagemagick \
  ffmpeg \
  texlive-full \
  git \
  golang-go \
  pdf2svg \
  build-essential \
  cabal-install
RUN go get arp242.net/singlepage
RUN apt-get install -y \
  libghc-zlib-dev
RUN cabal update \
  && cabal install \
    pandoc \
    pandoc-crossref \
    pandoc-citeproc \
    pandoc-include-code
ENV PATH="/root/.cabal/bin:${PATH}"
RUN apt-get install -y \
  python3-pip
RUN pip3 install \
  scipy \
  matplotlib \
  seaborn \
  pandoc-include
RUN apt-get install -y \
  curl \
  sketch
ENV max_print_line=1000
ENV error_line=254
ENV half_error_line=238
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs
ADD https://github.com/kohler/gifsicle/archive/v1.92.tar.gz /tmp/gifsicle.tar.gz
RUN apt-get install -y dh-autoreconf
RUN cd /tmp \
  && tar -xzf gifsicle.tar.gz \
  && cd gifsicle-1.92 \
  && autoreconf -i \
  && ./configure \
  && make install
RUN npm install -g gifify
COPY ImageMagick-policy.xml /etc/ImageMagick-6/policy.xml
ENV PATH="/root/.cabal/bin:/root/go/bin:${PATH}"
RUN apt-get install librsvg2-bin
WORKDIR /src