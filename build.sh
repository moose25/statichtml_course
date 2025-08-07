#!/bin/bash

# Build script for production deployment to GitHub Pages
# This builds the site with the correct base path for GitHub Pages

echo "Building site for production..."
python3 src/main.py "/statichtml_course/"
echo "Production build completed!"
