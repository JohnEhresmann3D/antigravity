#!/usr/bin/env python3
"""
Performance Dashboard Server
Real-time dashboard for monitoring code quality and performance analysis.
"""

from flask import Flask, render_template, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import os
import json
import subprocess
import threading
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'performance-dashboard-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
REPORTS_DIR = os.path.join(PROJECT_ROOT, "tools", "dashboard", "reports")
ANALYZER_PATH = os.path.join(PROJECT_ROOT, "tools", "analysis", "performance_analyzer.py")

# Global state
analysis_running = False

def get_latest_report():
    """Get the most recent performance report"""
    if not os.path.exists(REPORTS_DIR):
        return None
    
    reports = [f for f in os.listdir(REPORTS_DIR) if f.startswith('performance_report_') and f.endswith('.html')]
    if not reports:
        return None
    
    reports.sort(reverse=True)  # Most recent first
    return reports[0]

def get_all_reports():
    """Get list of all reports with metadata"""
    if not os.path.exists(REPORTS_DIR):
        return []
    
    reports = []
    for filename in os.listdir(REPORTS_DIR):
        if filename.startswith('performance_report_') and filename.endswith('.html'):
            filepath = os.path.join(REPORTS_DIR, filename)
            stat = os.stat(filepath)
            
            # Extract timestamp from filename
            timestamp_str = filename.replace('performance_report_', '').replace('.html', '')
            
            reports.append({
                'filename': filename,
                'timestamp': timestamp_str,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })
    
    reports.sort(key=lambda x: x['timestamp'], reverse=True)
    return reports

def get_report_summary(report_path):
    """Extract summary data from a report"""
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract JSON data from HTML
        import re
        match = re.search(r'const data = ({.*?});', content, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
            return {
                'overall_score': data.get('overall_score', 0),
                'total_files': data.get('total_files', 0),
                'total_issues': data.get('total_issues', 0),
                'high': data.get('issues_breakdown', {}).get('high', 0),
                'medium': data.get('issues_breakdown', {}).get('medium', 0),
                'low': data.get('issues_breakdown', {}).get('low', 0)
            }
    except Exception as e:
        print(f"Error reading report: {e}")
    
    return None

def run_analysis():
    """Run performance analysis in background"""
    global analysis_running
    
    try:
        analysis_running = True
        socketio.emit('analysis_started', {'message': 'Analysis started...'})
        
        # Run the analyzer
        result = subprocess.run(
            ['python', ANALYZER_PATH],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            socketio.emit('analysis_complete', {
                'message': 'Analysis complete!',
                'output': result.stdout
            })
        else:
            socketio.emit('analysis_error', {
                'message': 'Analysis failed',
                'error': result.stderr
            })
    
    except Exception as e:
        socketio.emit('analysis_error', {
            'message': 'Analysis failed',
            'error': str(e)
        })
    
    finally:
        analysis_running = False

@app.route('/')
def index():
    """Main dashboard page"""
    latest_report = get_latest_report()
    all_reports = get_all_reports()
    
    summary = None
    if latest_report:
        report_path = os.path.join(REPORTS_DIR, latest_report)
        summary = get_report_summary(report_path)
    
    return render_template('dashboard.html',
                         latest_report=latest_report,
                         all_reports=all_reports,
                         summary=summary)

@app.route('/api/reports')
def api_reports():
    """API endpoint to get all reports"""
    return jsonify(get_all_reports())

@app.route('/api/latest')
def api_latest():
    """API endpoint to get latest report info"""
    latest = get_latest_report()
    if latest:
        report_path = os.path.join(REPORTS_DIR, latest)
        summary = get_report_summary(report_path)
        return jsonify({
            'filename': latest,
            'summary': summary
        })
    return jsonify({'error': 'No reports found'}), 404

@app.route('/api/run-analysis', methods=['POST'])
def api_run_analysis():
    """API endpoint to trigger analysis"""
    global analysis_running
    
    if analysis_running:
        return jsonify({'error': 'Analysis already running'}), 409
    
    # Run in background thread
    thread = threading.Thread(target=run_analysis)
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Analysis started'})

@app.route('/reports/<path:filename>')
def serve_report(filename):
    """Serve report files"""
    return send_from_directory(REPORTS_DIR, filename)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to dashboard'})

if __name__ == '__main__':
    print("=" * 60)
    print("Performance Dashboard Server")
    print("=" * 60)
    print(f"Starting server on http://localhost:8080")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Reports directory: {REPORTS_DIR}")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server\n")
    
    socketio.run(app, host='localhost', port=8080, debug=False, allow_unsafe_werkzeug=True)
