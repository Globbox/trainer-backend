#!/bin/bash

cmd="$@"

export PYTHONPATH=${PYTHONPATH}:${PROJECT_ROOT}

echo Run command ${cmd}
exec ${cmd}
