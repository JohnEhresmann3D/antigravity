#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Analyzer - Uses local Ollama to analyze the Godot project structure and code.
"""

import sys
import os
import json
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Import our tools
try:
    from godot_ai_connector import GodotProjectAnalyzer
    from ollama_client import OllamaClient
except ImportError:
    print("Error: Could not import required modules. Make sure 'godot_ai_connector.py' and 'ollama_client.py' are in the same directory.")
    sys.exit(1)

def main():
    # Configuration
    model = "qwen2.5-coder:32b"  # Best model found locally
    project_root = os.getcwd()
    
    print(f"[*] Starting Project Analysis using {model}...")
    
    # 1. Analyze Project Structure
    print("[-] Gathering project metadata...")
    try:
        analyzer = GodotProjectAnalyzer(project_root)
        analysis_data = analyzer.analyze()
        
        # Simplify data for LLM context window if needed
        # For now, we'll send the summary which is relatively compact
        project_summary = json.dumps(analysis_data, indent=2)
        
    except Exception as e:
        print(f"[!] Analysis failed: {e}")
        sys.exit(1)

    # 2. Construct Prompt
    print("[-] Preparing prompt for Ollama...")
    
    system_prompt = """You are a senior Godot Game Developer and Software Architect. 
Your task is to analyze the provided Godot project structure and metadata.
Provide a comprehensive assessment including:
1. **Architecture Review**: Evaluate the organization of scenes and scripts.
2. **Code Quality**: Identify potential improvements based on script names and structure.
3. **Recommendations**: Suggest best practices or missing components for a game of this type.
4. **Next Steps**: Propose logical next steps for development.

Be concise, professional, and actionable."""

    user_prompt = f"""Here is the JSON summary of my Godot project:

{project_summary}

Please analyze this project."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # 3. Query Ollama
    print(f"[-] Sending request to Ollama (Model: {model})...")
    print("\n" + "="*80 + "\n")
    
    client = OllamaClient()
    
    try:
        # Stream the response
        full_response = ""
        for chunk in client.chat(messages, model=model, stream=True):
            if 'message' in chunk and 'content' in chunk['message']:
                content = chunk['message']['content']
                print(content, end='', flush=True)
                full_response += content
        
        print("\n\n" + "="*80 + "\n")
        print("[*] Analysis Complete.")
        
        # Optional: Save report
        with open("project_analysis_report.md", "w", encoding="utf-8") as f:
            f.write(f"# Project Analysis Report\n\nDate: {os.path.basename(os.getcwd())}\nModel: {model}\n\n")
            f.write(full_response)
        print("[-] Report saved to 'project_analysis_report.md'")

    except KeyboardInterrupt:
        print("\n[!] Analysis aborted by user.")
    except Exception as e:
        print(f"\n[!] Error during inference: {e}")

if __name__ == "__main__":
    main()
