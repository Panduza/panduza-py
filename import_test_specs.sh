#!/bin/bash

# Define branch and paths
BRANCH="main"
TEMP_DIR="tmp_dl_tests"
TARGET_DIR="tests/features"

# Create the target directory if it does not exist
if [ ! -d "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR"
    echo "Target directory created: $TARGET_DIR"
fi

# Remove the temporary directory if it already exists
if [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
fi

# Clone the full repository
echo "Cloning the repository (branch: $BRANCH)..."
git clone --branch "$BRANCH" --depth 1 git@github.com:Panduza/panduza-rust.git "$TEMP_DIR"

# Check if the clone was successful
if [ ! -d "$TEMP_DIR/tests/features" ]; then
    echo "Error: The 'tests/features' directory was not found in the cloned repository!"
    exit 1
fi

# Copy files from the features directory to the target directory
echo "Copying feature files..."
cp -R "$TEMP_DIR/tests/features/"* "$TARGET_DIR/"

# Clean up the temporary directory
echo "Cleaning up..."
rm -rf "$TEMP_DIR"

echo "Done! Feature files have been copied to $TARGET_DIR"
