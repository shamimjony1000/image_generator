document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('image-form');
    const generateBtn = document.getElementById('generate-btn');
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    const imageContainer = document.getElementById('image-container');
    const promptUsed = document.getElementById('prompt-used');
    const errorMessage = document.getElementById('error-message');
    const referenceImageInput = document.getElementById('reference_image');
    const imagePreview = document.getElementById('image-preview');
    
    // Handle image preview when a file is selected
    referenceImageInput.addEventListener('change', function() {
        // Clear previous preview
        imagePreview.innerHTML = '';
        
        if (this.files && this.files[0]) {
            const file = this.files[0];
            
            // Only process image files
            if (!file.type.match('image.*')) {
                imagePreview.innerHTML = '<p>Selected file is not an image</p>';
                return;
            }
            
            // Create image preview
            const img = document.createElement('img');
            img.file = file;
            imagePreview.appendChild(img);
            
            // Read the file and set the image source
            const reader = new FileReader();
            reader.onload = (function(aImg) { 
                return function(e) { 
                    aImg.src = e.target.result; 
                }; 
            })(img);
            reader.readAsDataURL(file);
        }
    });
    
    // Handle example prompt buttons
    document.querySelectorAll('.prompt-btn').forEach(button => {
        button.addEventListener('click', function() {
            const promptText = this.getAttribute('data-prompt');
            const promptTextarea = document.getElementById('prompt');
            
            // Set the textarea value to the selected prompt
            promptTextarea.value = promptText;
            
            // Highlight the active button
            document.querySelectorAll('.prompt-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
            
            // Scroll to the textarea and focus it
            promptTextarea.scrollIntoView({ behavior: 'smooth' });
            promptTextarea.focus();
        });
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading, hide results and errors
        loadingDiv.classList.remove('hidden');
        resultDiv.classList.add('hidden');
        errorDiv.classList.add('hidden');
        
        // Disable the generate button
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
        
        // Get form data
        const formData = new FormData(form);
        
        // Add a note to the loading message if using a reference image
        const referenceFile = referenceImageInput.files[0];
        if (referenceFile) {
            loadingDiv.querySelector('p').textContent = 'Generating your image based on the reference image...';
        } else {
            loadingDiv.querySelector('p').textContent = 'Generating your image...';
        }
        
        // Send the request to our Flask backend
        fetch('/generate', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            // Always parse the JSON, even for error responses
            return response.json().then(data => {
                // If response is not OK, throw an error with the data
                if (!response.ok) {
                    // Create an error object that includes both status and response data
                    const error = new Error(`HTTP error! Status: ${response.status}`);
                    error.responseData = data;
                    throw error;
                }
                return data;
            });
        })
        .then(data => {
            // Hide loading
            loadingDiv.classList.add('hidden');
            
            // Check if there's an error in the response
            if (data.error) {
                showError(data.error);
                return;
            }
            
            // Display the image
            displayImage(data);
        })
        .catch(error => {
            loadingDiv.classList.add('hidden');
            
            // Check if we have detailed response data from the API
            if (error.responseData) {
                let errorMessage = error.message;
                
                // Add API error details if available
                if (error.responseData.error) {
                    errorMessage += '\n\nAPI Error: ' + error.responseData.error;
                }
                
                // Add API response details if available
                if (error.responseData.details) {
                    errorMessage += '\n\nDetails: ' + error.responseData.details;
                }
                
                // If there's an api_response field, show that too
                if (error.responseData.api_response) {
                    errorMessage += '\n\nAPI Response: ' + JSON.stringify(error.responseData.api_response, null, 2);
                }
                
                showError(errorMessage);
            } else {
                showError(error.message || 'An unexpected error occurred');
            }
        })
        .finally(() => {
            // Re-enable the generate button
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate Image';
        });
    });
    
    function displayImage(data) {
        // Clear previous image
        imageContainer.innerHTML = '';
        
        // Check if the data contains the image URL
        if (data.image_url) {
            // Create image element
            const img = document.createElement('img');
            img.src = data.image_url;
            img.alt = 'Generated image';
            
            // Add image to container
            imageContainer.appendChild(img);
            
            // Display the prompt used
            promptUsed.textContent = `Prompt: "${data.prompt || 'Not provided'}"`;
            
            // Show the result
            resultDiv.classList.remove('hidden');
        } else {
            showError('No image URL was returned from the API');
        }
    }
    
    function showError(message) {
        errorMessage.textContent = message;
        errorDiv.classList.remove('hidden');
    }
});
