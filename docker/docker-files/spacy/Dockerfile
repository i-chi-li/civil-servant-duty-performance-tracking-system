# syntax=docker/dockerfile:1
FROM python:3.12-bookworm

RUN \
  --mount=type=cache,target=/var/lib/apt/lists \
  --mount=type=cache,target=/var/cache/apt/archives \
  --mount=type=cache,target=/root/.cache/pip \
  <<EOL
  # Setup
  set +eux
  # setup apt package repository
  sed -i 's#deb.debian.org/debian$#ftp.jp.debian.org/debian#' /etc/apt/sources.list.d/debian.sources
  apt-get update
  # Install pip packages
  pip install -U pip setuptools wheel
  pip install -U spacy
  #python -m spacy download en_core_web_sm
  python -m spacy download ja_core_news_lg
  echo "All done!"
EOL

CMD ["tail", "-f", "/dev/null"]
