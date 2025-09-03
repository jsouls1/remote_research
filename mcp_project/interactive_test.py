#!/usr/bin/env python3
import subprocess
import json
import sys

def test_tool(tool_name, arguments):
    process = subprocess.Popen(
        ['uv', 'run', 'research_server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Initialize
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"roots": {"listChanged": True}, "sampling": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }
        
        process.stdin.write(json.dumps(init_request) + '\n')
        process.stdin.flush()
        init_response = process.stdout.readline()
        
        # Send initialized notification
        process.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + '\n')
        process.stdin.flush()
        
        # Call tool
        tool_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        process.stdin.write(json.dumps(tool_request) + '\n')
        process.stdin.flush()
        
        tool_response = process.stdout.readline()
        if tool_response:
            response_data = json.loads(tool_response.strip())
            if 'result' in response_data:
                print(f"✅ Tool '{tool_name}' executed successfully!")
                print(f"Result: {response_data['result']['content'][0]['text']}")
            else:
                print(f"❌ Tool error: {response_data}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        process.terminate()

if __name__ == "__main__":
    print("Testing search_papers tool...")
    test_tool("search_papers", {"topic": "machine learning", "max_results": 2})