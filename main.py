from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import openai
import os

# Set up your OpenAI API key
openai.api_key = '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'

class ChatbotRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/exit':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open(os.path.join(os.getcwd(), 'exit.html'), 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open(os.path.join(os.getcwd(), 'index.html'), 'rb') as file:
                self.wfile.write(file.read())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        prompt = data.get('prompt', '')

        if prompt.lower() == 'quit':
            # Serve the exit.html page
            self.send_response(301)
            self.send_header('Location', '/exit')
            self.end_headers()
        else:
            # Generate response from OpenAI
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=2000  # Adjust as needed
            ).choices[0].text.strip()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'response': response}).encode('utf-8'))

def run_server():
    server_address = ('', 5001)
    httpd = HTTPServer(server_address, ChatbotRequestHandler)
    print('Server running at http://localhost:5001')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()