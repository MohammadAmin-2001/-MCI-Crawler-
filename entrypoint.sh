#!/bin/sh
set -e

echo "Starting Xvfb..."

Xvfb :99 \
    -screen 0 1366x768x24 \
    -ac \
    -nolisten tcp &

export DISPLAY=:99

sleep 2

echo "DISPLAY=$DISPLAY"

if ! kill -0 $! 2>/dev/null; then
    echo "Xvfb failed to start"
    exit 1
fi

echo "Xvfb is running"
echo "Starting Python..."

exec python3 -u main.py