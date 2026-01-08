#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama Client - Simple Python client for interacting with local Ollama instance.
No external dependencies required (uses standard urllib).

Usage:
    python ollama_client.py --prompt "Why is the sky blue?" --model "llama3"
"""

import sys
import json
import argparse
import urllib.request
import urllib.error
from typing import Dict, Any, Generator, Optional, List

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip('/')
    
    def _post(self, endpoint: str, data: Dict[str, Any], stream: bool = False) -> Any:
        """Send POST request to Ollama API"""
        url = f"{self.base_url}{endpoint}"
        
        # Ensure stream is set correctly in data if not present
        if 'stream' not in data:
            data['stream'] = stream
            
        try:
            json_data = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(
                url, 
                data=json_data, 
                headers={'Content-Type': 'application/json'}
            )
            
            response = urllib.request.urlopen(req)
            
            if stream:
                return self._stream_response(response)
            else:
                return json.loads(response.read().decode('utf-8'))
                
        except urllib.error.URLError as e:
            print(f"Error connecting to Ollama at {self.base_url}: {e}")
            if hasattr(e, 'read'):
                print(e.read().decode('utf-8'))
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def _stream_response(self, response) -> Generator[Dict[str, Any], None, None]:
        """Yield parsed JSON objects from streaming response"""
        for line in response:
            line = line.decode('utf-8').strip()
            if line:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    pass

    def generate(self, prompt: str, model: str = "llama3", stream: bool = False, **kwargs) -> Any:
        """
        Generate text completion
        
        Args:
            prompt: Input text
            model: Model name to use
            stream: Whether to stream response
            **kwargs: Additional parameters for Ollama (options, system, etc.)
        """
        data = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            **kwargs
        }
        return self._post("/api/generate", data, stream)

    def chat(self, messages: List[Dict[str, str]], model: str = "llama3", stream: bool = False, **kwargs) -> Any:
        """
        Chat with model
        
        Args:
            messages: List of message dicts (role, content)
            model: Model name
            stream: Whether to stream response
            **kwargs: Additional parameters
        """
        data = {
            "model": model,
            "messages": messages,
            "stream": stream,
            **kwargs
        }
        return self._post("/api/chat", data, stream)

    def list_models(self) -> List[str]:
        """Get list of available locally installed models"""
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags")
            response = urllib.request.urlopen(req)
            data = json.loads(response.read().decode('utf-8'))
            return [model['name'] for model in data.get('models', [])]
        except Exception as e:
            print(f"Failed to list models: {e}")
            return []


def main():
    """CLI Entry Point"""
    parser = argparse.ArgumentParser(description="Ollama Python Client")
    parser.add_argument("--prompt", "-p", help="Text prompt to send")
    parser.add_argument("--model", "-m", default="llama3", help="Model name (default: llama3)")
    parser.add_argument("--url", default="http://localhost:11434", help="Ollama API URL")
    parser.add_argument("--list", "-l", action="store_true", help="List available models")
    parser.add_argument("--stream", "-s", action="store_true", help="Stream output")
    parser.add_argument("--system", help="System prompt")
    
    args = parser.parse_args()
    
    client = OllamaClient(base_url=args.url)
    
    if args.list:
        print("Available models:")
        models = client.list_models()
        if models:
            for m in models:
                print(f"  - {m}")
        else:
            print("  No models found or connection failed.")
        return

    if args.prompt:
        print(f"Sending prompt to {args.model}...\n")
        
        options = {}
        if args.system:
            options['system'] = args.system
            
        if args.stream:
            # Streaming mode
            try:
                for chunk in client.generate(args.prompt, model=args.model, stream=True, **options):
                    if 'response' in chunk:
                        print(chunk['response'], end='', flush=True)
                print() # Newline at end
            except KeyboardInterrupt:
                print("\nAborted.")
        else:
            # Non-streaming mode
            response = client.generate(args.prompt, model=args.model, stream=False, **options)
            if response and 'response' in response:
                print(response['response'])
            else:
                print("No response received.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
