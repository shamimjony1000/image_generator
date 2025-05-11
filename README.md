# AI Image Generator

A Flask-based web application that generates images using AI through the agent.ai API.

## Features

- Simple and intuitive user interface
- Generate images with customizable parameters
- Support for different aspect ratios and styles
- Responsive design that works on desktop and mobile

## Live Demo
https://image.parviit.com

## Requirements

- Python 3.7+
- Flask
- Requests

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd "Image generator"
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Usage

1. Enter a descriptive prompt for the image you want to generate
2. Select your preferred model (currently only DALL-E 3 is supported)
3. Choose a style (default, vivid, or natural)
4. Select an aspect ratio (portrait, square, or landscape)
5. Click "Generate Image" and wait for your image to be created

## API Configuration

The application uses the agent.ai API for image generation. The API key is already configured in the application.

## License

This project is open source and available under the MIT License.
