#!/bin/bash

# Script to run the Movie Hangman game with proper setup

# Change to the game directory
cd "$(dirname "$0")"

# Check if Pygame is installed
python3 -c "import pygame" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Pygame is not installed. Would you like to install it? (y/n)"
    read answer
    if [ "$answer" = "y" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        echo "Installing pygame..."
        pip install pygame
    else
        echo "Pygame is required to run this game. Exiting."
        exit 1
    fi
else
    echo "Pygame is already installed."
fi

# Check if image files exist, create them if they don't
if [ ! -f "worried_kangaroo.png" ] || [ ! -f "happy_kangaroo.png" ] || [ ! -f "sad_kangaroo.png" ] || [ ! -f "noose.png" ]; then
    echo "Image files not found. Creating them now..."
    python3 create_png_images.py
fi

# Run the game
echo "Starting Movie Hangman game..."
python3 movie_hangman.py

# Exit message
echo "Thanks for playing!"
