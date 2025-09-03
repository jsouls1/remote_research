#!/usr/bin/env python3
import subprocess
import json
import sys

def test_mcp_server():
    # Start the server process
    process = subprocess.Popen(
        ['uv', 'run', 'research_server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Send initialization
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {"listChanged": True},
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        process.stdin.write(json.dumps(init_request) + '\n')
        process.stdin.flush()
        
        # Read response
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print("✅ Server initialized successfully!")
            print(f"Server: {response['result']['serverInfo']['name']}")
            
            # Send initialized notification
            initialized_notification = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            }
            
            process.stdin.write(json.dumps(initialized_notification) + '\n')
            process.stdin.flush()
            
            # Test tools/list
            tools_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            }
            
            process.stdin.write(json.dumps(tools_request) + '\n')
            process.stdin.flush()
            
            tools_response = process.stdout.readline()
            if tools_response:
                tools_data = json.loads(tools_response.strip())
                if 'result' in tools_data and 'tools' in tools_data['result']:
                    print(f"✅ Found {len(tools_data['result']['tools'])} tools:")
                    for tool in tools_data['result']['tools']:
                        print(f"  - {tool['name']}: {tool['description']}")
                else:
                    print(f"❌ Unexpected tools response: {tools_data}")
            
        else:
            print("❌ No response from server")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        process.terminate()

if __name__ == "__main__":
    test_mcp_server()