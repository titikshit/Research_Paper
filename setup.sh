#!/bin/bash

# setup.sh - Script to set up the Research Paper Metadata Extractor

# Exit immediately if a command exits with a non-zero status.
set -e

echo "=== Research Paper Metadata Extractor Setup ==="

# 1. Check for Python 3 installation
if ! command -v python3 &> /dev/null
then
    echo "Python 3 could not be found. Please install Python 3.6 or higher."
    exit 1
fi

echo "Python 3 is installed."

# 2. Check for Git installation
if ! command -v git &> /dev/null
then
    echo "Git could not be found. Please install Git."
    exit 1
fi

echo "Git is installed."

# 3. Set up a virtual environment
echo "Setting up virtual environment..."
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

echo "Virtual environment activated."

# 4. Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. Check for Docker installation
if ! command -v docker &> /dev/null
then
    echo "Docker could not be found. Please install Docker before proceeding."
    deactivate
    exit 1
fi

echo "Docker is installed."

# 6. Pull and run GROBID Docker container
echo "Pulling GROBID Docker image..."
docker pull lfoppiano/grobid:0.7.2

echo "Running GROBID Docker container..."
docker run -d --name grobid -p 8070:8070 lfoppiano/grobid:0.7.2

echo "GROBID is running."

# 7. Run the Streamlit app
echo "Starting the Streamlit app..."
streamlit run app.py