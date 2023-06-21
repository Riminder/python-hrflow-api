#!/bin/bash

BUMP_MAJOR="major"
BUMP_MINOR="minor"
BUMP_PATCH="patch"

DEFAULT_BUMP=$BUMP_PATCH

# Parse argument to get the bump type
if [ $# -eq 0 ]; then
    BUMP=$DEFAULT_BUMP
else
    BUMP=$1
fi

# Get the latest tag using `git describe`
LATEST_TAG=$(git describe --abbrev=0 --tags)

# Extract version numbers from the latest tag
VERSION=$(echo "$LATEST_TAG" | sed 's/v//')

# Split version into major, minor, and patch components
IFS='.' read -ra VERSION_ARRAY <<< "$VERSION"
MAJOR=${VERSION_ARRAY[0]}
MINOR=${VERSION_ARRAY[1]}
PATCH=${VERSION_ARRAY[2]}

# Increment the version based on the bump type
if [ "$BUMP" = "$BUMP_MAJOR" ]; then
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
elif [ "$BUMP" = "$BUMP_MINOR" ]; then
    MINOR=$((MINOR + 1))
    PATCH=0
elif [ "$BUMP" = "$BUMP_PATCH" ]; then
    PATCH=$((PATCH + 1))
else
    echo "Unknown bump type. Please use either 'major', 'minor', or 'patch'."
    exit 1
fi

# Construct the new tag
NEW_TAG="v$MAJOR.$MINOR.$PATCH"
echo $NEW_TAG