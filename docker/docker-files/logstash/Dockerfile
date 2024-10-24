# syntax=docker/dockerfile:1
FROM docker.elastic.co/logstash/logstash:${STACK_VERSION}

RUN <<EOL
  set +eux
  elasticsearch-plugin install ingest-attachment
EOL
