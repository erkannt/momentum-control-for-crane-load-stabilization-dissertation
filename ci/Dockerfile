FROM debian:10-slim AS pandoc-build
RUN apt-get update && apt-get install -y \
  cabal-install \
  libghc-zlib-dev
RUN cabal update \
  && cabal install -j4 \
    pandoc \
    pandoc-crossref \
    pandoc-citeproc \
    pandoc-include-code

FROM golang AS singlepage-build
RUN go get arp242.net/singlepage

FROM debian:10-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
  curl \
  dh-autoreconf \
  python3-pip \
  python3-setuptools \
  imagemagick \
  ffmpeg \
  pdf2svg \
  librsvg2-bin \
  sketch \
  && apt-get autoremove && apt-get autoclean \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
  scipy \
  matplotlib \
  seaborn \
  pandoc-include

ADD https://github.com/kohler/gifsicle/archive/v1.92.tar.gz /tmp/gifsicle.tar.gz
RUN cd /tmp \
  && tar -xzf gifsicle.tar.gz \
  && cd gifsicle-1.92 \
  && autoreconf -i \
  && ./configure \
  && make install

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y --no-install-recommends nodejs
RUN npm install -g gifify

COPY ImageMagick-policy.xml /etc/ImageMagick-6/policy.xml

RUN apt-get install -y \
  texlive-fonts-recommended \
  texlive-latex-extra \
  texlive-lang-korean \
  texlive-science \
  texlive-extra-utils \
  texlive-base \
  && apt-get autoremove && apt-get autoclean \
  && rm -rf /var/lib/apt/lists/*
# latexrun can't handle linebreaks in latex output
ENV max_print_line=1000
ENV error_line=254
ENV half_error_line=238

COPY --from=pandoc-build /root/.cabal/bin /root/.cabal/bin
COPY --from=pandoc-build /root/.cabal/share /root/.cabal/share
COPY --from=singlepage-build /go/bin/singlepage /usr/local/bin/singlepage
ENV PATH="/root/.cabal/bin:${PATH}"

WORKDIR /src
