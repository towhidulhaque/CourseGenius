#!/usr/bin/env sh

celery -A server  worker -l  info
