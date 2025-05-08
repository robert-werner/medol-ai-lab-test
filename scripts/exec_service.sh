#!/bin/bash

# shellcheck disable=SC2086
fastapi run --host 0.0.0.0 --port 8080 /opt/vkr-frontend/frontend/main.py
