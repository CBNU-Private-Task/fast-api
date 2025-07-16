from fastapi import FastAPI
import requests
import json
from typing import Optional
import os
import json
from pathlib import Path

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/greet")
def greet_user(name: str):
    return {"message": "Hello, " + name + "!"}

@app.post("/ollama")
def call_ollama(prompt: str, write_to_file: Optional[bool] = True):
    
    url = "http://ollama.ksga.info/api/chat"
   
    enhanced_system_prompt = """You are a JavaScript code generator. Follow these rules strictly:

    1. ONLY return executable JavaScript code
    2. NO explanations, NO descriptions, NO markdown formatting
    3. NO code blocks (```), NO backticks
    4. Use proper JavaScript syntax with semicolons
    5. Use // for single-line comments, /* */ for multi-line comments
    6. If you need to explain something, use JavaScript comments only
    7. Each statement should be on its own line
    8. Ensure all code is valid and executable JavaScript
    9. Start writing code immediately, no preamble

    Example of correct format:
    // This function adds two numbers
    function addNumbers(a, b) {
        return a + b;
    }

    // Usage example
    console.log(addNumbers(5, 3));"""

    requestBody = {
        "model": "llama3-backup:latest",
        "messages": [
            {
                "role": "system",
                "content": enhanced_system_prompt,
            },
            {
                "role": "user", 
                "content": f"Generate JavaScript code for: {prompt}. Remember: ONLY JavaScript code with proper syntax, use comments for any explanations.",
            },
        ],
        "stream": False,
        "temperature": 0.3,
    }
    
    try:
        response = requests.post(url, json=requestBody)
        ollama_response = response.json()
        
        ai_content = ""
        if "message" in ollama_response and "content" in ollama_response["message"]:
            ai_content = ollama_response["message"]["content"]
            
            ai_content = clean_javascript_response(ai_content, prompt) 
        
        
        # Trigger VS Code file write
        vscode_trigger_result = None
        if write_to_file and ai_content:
            print("Triggering VS Code file write...")
            vscode_trigger_result = trigger_vscode_file_write(prompt, ai_content)
        
        return {
            "success": True,
            "prompt": prompt,
            "response": ollama_response,
            "ai_content": ai_content,
            "file_written": write_to_file,
            "vscode_trigger_result": vscode_trigger_result
        }
        
    except ValueError as ve:
        print(f"JSON parsing error: {ve}")
        return {"error": "Invalid JSON response", "raw_text": response.text}
    except Exception as e:
        print(f"General error: {e}")
        return {"error": str(e)}

def clean_javascript_response(content: str, original_prompt: str) -> str:  
    """
    Clean the AI response to ensure it's pure JavaScript code
    """
    content = content.replace("```javascript", "").replace("```js", "").replace("```", "")

    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        
        if not line and not cleaned_lines:
            continue
            
        if line.startswith("Here") or line.startswith("This") or line.startswith("The"):
            if not line.startswith("//"):
                line = f"// {line}"
        
        cleaned_lines.append(line)
    
    cleaned_content = '\n'.join(cleaned_lines).strip()
    
    if cleaned_content:
        header = f"//Request: {original_prompt[:50]}{'...' if len(original_prompt) > 50 else ''}\n\n"
        cleaned_content = header + cleaned_content
    
    return cleaned_content

def get_vscode_server_port():
    """
    Read the VS Code extension server port from config file
    """
    try:
        config_dir = Path.home() / '.vscode-streaming-extension'
        config_path = config_dir / 'server-config.json'
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
                port = config.get('port')
                status = config.get('status')
                
                if port and status == 'running':
                    print(f"✅ Found VS Code server on port {port}")
                    return port
                else:
                    print(f"❌ VS Code server not running (status: {status})")
                    return None
        else:
            print("❌ VS Code server config not found")
            return None
            
    except Exception as e:
        print(f"❌ Error reading VS Code server config: {e}")
        return None

def trigger_vscode_file_write(prompt: str, ai_content: str):
    """
    Triggers the VS Code extension to write content to file
    """
    try:
        # Get the dynamic port
        port = get_vscode_server_port()
        if not port:
            return {"success": False, "error": "VS Code server not running or port not found"}
        
        vscode_payload = {
            "prompt": prompt,
            "content": ai_content,
            "action": "write_to_file"
        }
        
        url = f"http://localhost:{port}/write-file"
        print(f"Sending to VS Code server at: {url}")
        
        response = requests.post(url, json=vscode_payload, timeout=10)
        
        print(f"VS Code response status: {response.status_code}")
        print(f"VS Code response: {response.text}")
        
        return {
            "success": True,
            "status_code": response.status_code,
            "response": response.text,
            "port_used": port
        }
        
    except requests.exceptions.ConnectionError as ce:
        error_msg = f"Could not connect to VS Code server: {ce}"
        print(error_msg)
        return {"success": False, "error": error_msg}
    except Exception as e:
        error_msg = f"Error triggering VS Code file write: {e}"
        print(error_msg)
        return {"success": False, "error": error_msg}

# Enhanced test endpoint
@app.get("/test-vscode-connection")
def test_vscode_connection():
    try:
        port = get_vscode_server_port()
        if not port:
            return {"vscode_server": "not_running", "error": "Server config not found"}
        
        response = requests.get(f"http://localhost:{port}/health", timeout=5)
        return {
            "vscode_server": "connected", 
            "port": port,
            "status": response.status_code,
            "response": response.json()
        }
    except Exception as e:
        return {"vscode_server": "not_connected", "error": str(e)}
