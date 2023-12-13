#!/bin/bash

PYTEST_RUN="poetry run pytest"
PYTEST_OPTIONS=(--verbose --tb=long --strict-markers)
PYTEST_DIR=tests/

if [ "$#" -gt 0 ]; then
    for marker in "$@"; do
        $PYTEST_RUN "${PYTEST_OPTIONS[@]}" "$PYTEST_DIR" -m "$marker"
    done
else
    $PYTEST_RUN "${PYTEST_OPTIONS[@]}" "$PYTEST_DIR"
fi
