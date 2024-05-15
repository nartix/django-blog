#!/bin/bash

# chmod +x build_css_js.sh
# ./build_css_js.sh

# Step 1: Run npm build inside Docker container
docker exec vitejs npm run --prefix /app/portfolio build

# Check if the build command was successful
if [ $? -eq 0 ]; then
    echo "Build successful. Proceeding with file copying..."

    # Define source and target directories for JS and CSS
    src_js_dir="vitejs/portfolio/dist/assets"
    target_js_dir="ferozfaiz/core/static/js"
    src_css_dir="vitejs/portfolio/dist/assets"
    target_css_dir="ferozfaiz/core/static/css"

    # Copy and rename JS file
    cp -f ${src_js_dir}/main-*.js ${target_js_dir}/index.js

    # Copy and rename CSS file
    cp -f ${src_css_dir}/main-*.css ${target_css_dir}/index.css

    echo "Files copied successfully."
else
    echo "Build failed. Please check the build logs for errors."
fi
