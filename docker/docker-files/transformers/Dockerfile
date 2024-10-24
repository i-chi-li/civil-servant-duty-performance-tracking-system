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
  # Install apt packages
  apt-get install -y ffmpeg tesseract-ocr

  # Install pip packages
  pip install --root-user-action ignore -U pip setuptools wheel
  pip install --root-user-action ignore \
    torch-directml \
    transformers \
    accelerate \
    datasets \
    librosa \
    soundfile \
    pytesseract \
    bitsandbytes \
    evaluate \
    seqeval \
    sacrebleu \
    rouge_score \
    jiwer \
    pytorchvideo \
    timm \
    albumentations \
    tensorboard \
    speechbrain \
    sentencepiece
EOL

ENV LD_LIBRARY_PATH=/usr/lib/wsl/lib

CMD ["tail", "-f", "/dev/null"]
