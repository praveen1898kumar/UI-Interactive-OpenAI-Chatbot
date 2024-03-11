from http.server import BaseHTTPRequestHandler, HTTPServer  # Import necessary modules for handling HTTP requests
import json  # Import module for JSON manipulation
import openai  # Import OpenAI library for accessing GPT-3
import os  # Import module for interacting with the operating system

# Set up your OpenAI API key
openai.api_key = '<open-ai-api-key>'  # Replace this with your own API key

class ChatbotRequestHandler(BaseHTTPRequestHandler):
    # Define handler for GET requests
    def do_GET(self):
        if self.path == '/exit':  # Check if the requested path is '/exit'
            # Send HTTP response with status code 200 and content type text/html
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Read and send the content of exit.html file
            with open(os.path.join(os.getcwd(), 'exit.html'), 'rb') as file:
                self.wfile.write(file.read())
        else:  # If the requested path is not '/exit'
            # Send HTTP response with status code 200 and content type text/html
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Read and send the content of index.html file
            with open(os.path.join(os.getcwd(), 'index.html'), 'rb') as file:
                self.wfile.write(file.read())

    # Define handler for POST requests
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # Extract content length from request headers
        post_data = self.rfile.read(content_length)  # Read POST data from request
        data = json.loads(post_data.decode('utf-8'))  # Decode JSON data from POST request

        prompt = data.get('prompt', '')  # Extract 'prompt' value from JSON data

        if prompt.lower() == 'quit':  # Check if prompt is 'quit'
            # Redirect the client to '/exit' page using HTTP status code 301
            self.send_response(301)
            self.send_header('Location', '/exit')
            self.end_headers()
        else:  # If prompt is not 'quit'
            # Generate response from OpenAI's GPT-3.5 engine
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=2000  # Adjust as needed
            ).choices[0].text.strip()

            # Send HTTP response with status code 200 and content type application/json
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Send the generated response back to the client as JSON data
            self.wfile.write(json.dumps({'response': response}).encode('utf-8'))

# Function to run the HTTP server
def run_server():
    server_address = ('', 5001)  # Define server address and port
    httpd = HTTPServer(server_address, ChatbotRequestHandler)  # Create HTTP server instance
    print('Server running at http://localhost:5001')  # Print server URL
    httpd.serve_forever()  # Keep the server running indefinitely

# Entry point of the program
if __name__ == '__main__':
    run_server()  # Run the HTTP server
