import sys
import os

# Print debugging information
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path}")

# Try importing the modules with error handling
try:
    import requests
    print(f"Successfully imported requests version: {requests.__version__}")
except ImportError as e:
    print(f"Error importing requests: {e}")
    print("Attempting to install requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    print("Retrying import...")
    import requests

try:
    import base64
    from io import BytesIO
    from flask import Flask, render_template, request, jsonify, url_for
    print("Successfully imported Flask and other modules")
except ImportError as e:
    print(f"Error importing Flask or other modules: {e}")
    print("Attempting to install Flask...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Flask"])
    print("Retrying import...")
    from flask import Flask, render_template, request, jsonify, url_for

app = Flask(__name__)

# API configuration
API_KEY = "CkBReIqmUkX88osNL7T5ntzdd8uIsgxPMgRqjIw3WU3pawoZ5M4L91kChMG5gjtw"
API_URL = "https://api-lr.agent.ai/v1/action/generate_image"

@app.route('/')
def index():
    """Render the main page of the application."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    """Generate an image based on the provided prompt and parameters."""
    try:
        # Get data from the form
        prompt = request.form.get('prompt')
        model = request.form.get('model', 'DALL-E 3')
        model_style = request.form.get('model_style', 'default')
        model_aspect_ratio = request.form.get('model_aspect_ratio', '9:16')
        
        # Check if a reference image was uploaded
        reference_image_base64 = None
        if 'reference_image' in request.files and request.files['reference_image'].filename:
            reference_file = request.files['reference_image']
            # Read the file and convert to base64
            file_content = reference_file.read()
            reference_image_base64 = base64.b64encode(file_content).decode('utf-8')
            print(f"Reference image uploaded: {reference_file.filename}")
        
        # Print the received form data for debugging
        print(f"Received form data: prompt='{prompt}', model='{model}', style='{model_style}', ratio='{model_aspect_ratio}', has_reference_image={reference_image_base64 is not None}")
        
        # Prepare the request payload
        payload = {
            "prompt": prompt,
            "model": model,
            "model_style": model_style,
            "model_aspect_ratio": model_aspect_ratio
        }
        
        # Add reference image to payload if provided
        if reference_image_base64:
            payload["reference_image"] = reference_image_base64
        
        # Set up headers exactly as shown in the curl example
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Print the request details for debugging
        print(f"API URL: {API_URL}")
        print(f"Headers: {headers}")
        print(f"Payload: {payload}")
        
        # Make the API request with better error handling
        try:
            print("Attempting to make API request...")
            print(f"API URL: {API_URL}")
            print(f"Headers: {headers}")
            print(f"Payload: {payload}")
            
            # For debugging, let's create a mock successful response
            # This will help us test the frontend without relying on the API
            mock_response = {
                "image_url": "https://via.placeholder.com/512x512.png?text=Generated+Image+Placeholder",
                "prompt": prompt
            }
            
            # Return the mock response for testing
            print("Using mock response for testing")
            return jsonify(mock_response)
            
            # Uncomment the below code when the API is working correctly
            '''
            response = requests.post(API_URL, json=payload, headers=headers)
            
            # Debug: Print response details
            print(f"API Response Status: {response.status_code}")
            print(f"API Response Headers: {response.headers}")
            '''
        except Exception as request_error:
            print(f"Error making API request: {str(request_error)}")
            import traceback
            traceback.print_exc()
            
            # Return a helpful error message and a placeholder image
            return jsonify({
                "image_url": "https://via.placeholder.com/512x512.png?text=API+Request+Error",
                "error": f"Error making API request: {str(request_error)}",
                "prompt": prompt
            })
        
        # The code below is commented out since we're using a mock response for testing
        # Once the API connection is fixed, you can uncomment this section and comment out the mock response above
        
        '''
        # Try to get the response text, but handle potential errors
        try:
            response_text = response.text
            print(f"API Response Content: {response_text}")
        except Exception as e:
            print(f"Error getting response text: {str(e)}")
            response_text = "<Could not read response text>"
        
        # Try to parse the JSON response, but handle potential errors
        try:
            if response.status_code == 200:
                result = response.json()
                print(f"Parsed JSON: {result}")
                
                # Now that we know the frontend works, let's process the actual API response
                processed_result = {}
                
                # Check for image URL in various possible locations in the response
                if 'image_url' in result:
                    processed_result['image_url'] = result['image_url']
                elif 'url' in result:
                    processed_result['image_url'] = result['url']
                elif 'data' in result and isinstance(result['data'], dict):
                    if 'url' in result['data']:
                        processed_result['image_url'] = result['data']['url']
                    elif 'image_url' in result['data']:
                        processed_result['image_url'] = result['data']['image_url']
                elif 'data' in result and isinstance(result['data'], list) and len(result['data']) > 0:
                    if isinstance(result['data'][0], dict):
                        if 'url' in result['data'][0]:
                            processed_result['image_url'] = result['data'][0]['url']
                        elif 'image_url' in result['data'][0]:
                            processed_result['image_url'] = result['data'][0]['image_url']
                
                # If we still couldn't find an image URL, check for any URL-like string in the response
                if 'image_url' not in processed_result:
                    # Try to find any URL in the response that looks like an image
                    import re
                    url_pattern = re.compile(r'https?://\S+\.(?:jpg|jpeg|png|gif|webp)', re.IGNORECASE)
                    for key, value in result.items():
                        if isinstance(value, str) and url_pattern.search(value):
                            processed_result['image_url'] = url_pattern.search(value).group(0)
                            break
                
                # Include the prompt in the response
                processed_result['prompt'] = prompt
                
                # If we still couldn't find an image URL, use a fallback for now
                if 'image_url' not in processed_result:
                    print("Warning: Could not find image URL in the API response")
                    # Return the full API response for debugging, but include a fallback image
                    processed_result['image_url'] = "https://via.placeholder.com/512x512.png?text=API+Response+Missing+Image+URL"
                    processed_result['api_response'] = result
                
                return jsonify(processed_result)
            else:
                # For non-200 responses, try to parse the error response
                try:
                    error_json = response.json()
                    return jsonify({
                        "error": f"API request failed with status code {response.status_code}",
                        "api_error": error_json
                    }), 500
                except:
                    # If we can't parse the JSON, return the raw text
                    return jsonify({
                        "error": f"API request failed with status code {response.status_code}",
                        "details": response_text
                    }), 500
        except Exception as json_error:
            print(f"Error parsing JSON response: {str(json_error)}")
            return jsonify({
                "error": "Failed to parse API response",
                "details": str(json_error),
                "raw_response": response_text
            }), 500
        '''
            
    except Exception as e:
        print(f"Exception in generate_image: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
