#!/usr/bin/env sh

celery -A server  beat -l  info
