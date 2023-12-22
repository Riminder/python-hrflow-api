#!/bin/bash

PYTEST_RUN="poetry run pytest"
PYTEST_OPTIONS=(--verbose --tb=long --strict-markers --durations=0 --datefmt "%Y-%m-%d %H:%M:%S.%f%z")
PYTEST_DIR=tests/

if [ "$#" -gt 0 ]; then
    for marker in "$@"; do
        $PYTEST_RUN "${PYTEST_OPTIONS[@]}" "$PYTEST_DIR" -m "$marker"
    done
else
    $PYTEST_RUN "${PYTEST_OPTIONS[@]}" "$PYTEST_DIR"
fi
