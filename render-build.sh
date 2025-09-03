#!/bin/bash
# apt-get update
# xargs -a apt.txt apt-get install -y

# apt-get update
# xargs -a apt.txt apt-get install -y
#!/usr/bin/env bash
set -euxo pipefail

# Install Python deps
pip install -r requirements.txt

# Install system deps for Chromium
apt-get update && apt-get install -y \
    libgtk-4-1 \
    libgraphene-1.0-0 \
    libgstreamer-gl1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    libenchant-2-2 \
    libsecret-1-0 \
    libmanette-0.2-0 \
    libgles2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    libnss3 \
    libxss1 \
    libxtst6 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2

# Install Chromium for Playwright
playwright install chromium --with-deps



pip install -r requirements.txt
playwright install

