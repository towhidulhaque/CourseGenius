#!/usr/bin/env sh

daphne server.asgi:application --bind 0.0.0.0 --port 9000
