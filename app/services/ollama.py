import requests
from ..core.config import settings
from .vscode import trigger_vscode_file_write

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

def call_ollama_service(prompt: str, write_to_file: bool):
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
        response = requests.post(settings.OLLAMA_API_URL, json=requestBody)
        ollama_response = response.json()
        
        ai_content = ""
        if "message" in ollama_response and "content" in ollama_response["message"]:
            ai_content = ollama_response["message"]["content"]
            ai_content = clean_javascript_response(ai_content, prompt)
        
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