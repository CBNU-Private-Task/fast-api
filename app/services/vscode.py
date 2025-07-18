import requests
import json
from pathlib import Path
from ..core.config import settings

def get_vscode_server_port():
    """
    Read the VS Code extension server port from config file
    """
    try:
        config_dir = Path(settings.VSCODE_SERVER_CONFIG_DIR)
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