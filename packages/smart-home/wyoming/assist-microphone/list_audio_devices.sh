#!/usr/bin/env bash
# wyoming-assist-microphone

set -exo pipefail

echo "RECORDING DEVICES:"
arecord -L

echo "PLAYING DEVICES:"
aplay -L
