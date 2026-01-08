#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Godot Performance Analyzer
Statically analyzes GDScript files for common performance pitfalls and best practice violations.
Generates an interactive HTML report.
"""

import os
import re
import json
import math
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# --- Configuration ---
PROJECT_ROOT = os.getcwd()
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

# Create reports directory if it doesn't exist
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

# Generate timestamped filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_FILE = os.path.join(REPORTS_DIR, f"performance_report_{timestamp}.html")
LATEST_LINK = os.path.join(PROJECT_ROOT, "performance_report.html")

# --- Analysis Rules ---
EXPENSIVE_CALLS = [
    r'(?<!\.)get_node\(',  # get_node("...")
    r'(?<!\.)\$',          # $Node
    r'ResourceLoader\.load',
    r'\.new\(',            # Creating new objects
]

# --- Templates ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Godot Performance Analysis Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-color: #1e1e1e;
            --text-color: #e0e0e0;
            --card-bg: #2d2d2d;
            --accent: #47a6ff;
            --danger: #ff5252;
            --warning: #ffb142;
            --success: #2cc990;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1, h2, h3 { color: var(--accent); }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .card { background-color: var(--card-bg); padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .score-card { text-align: center; }
        .score { font-size: 3em; font-weight: bold; }
        .score.good { color: var(--success); }
        .score.medium { color: var(--warning); }
        .score.bad { color: var(--danger); }
        
        .file-list { display: flex; flex-direction: column; gap: 10px; }
        .file-item { background-color: var(--card-bg); border-radius: 8px; overflow: hidden; }
        .file-header { 
            padding: 15px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            cursor: pointer; 
            background-color: #333;
        }
        .file-header:hover { background-color: #3d3d3d; }
        .file-name { font-weight: bold; font-family: monospace; }
        .file-score { padding: 5px 10px; border-radius: 4px; font-weight: bold; background: #444; }
        
        .file-details { padding: 15px; display: none; border-top: 1px solid #444; }
        .file-details.open { display: block; }
        
        .issue { margin-bottom: 10px; padding: 8px; border-left: 3px solid; background: rgba(0,0,0,0.2); }
        .issue.high { border-color: var(--danger); }
        .issue.medium { border-color: var(--warning); }
        .issue.low { border-color: var(--accent); }
        .issue-line { font-family: monospace; color: #aaa; margin-right: 10px; }
        .issue-type { font-weight: bold; margin-right: 10px; }
        .code-snippet { 
            font-family: monospace; 
            background: #111; 
            padding: 10px; 
            margin-top: 5px; 
            color: #ccc; 
            overflow-x: auto;
            white-space: pre;
        }
        .highlight { color: #fff; font-weight: bold; background: rgba(255, 82, 82, 0.2); }
        
        /* Filter controls */
        .filter-controls {
            margin: 20px 0;
            padding: 15px;
            background: var(--card-bg);
            border-radius: 8px;
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .filter-btn {
            padding: 8px 16px;
            border: 2px solid transparent;
            border-radius: 4px;
            background: #444;
            color: #fff;
            cursor: pointer;
            transition: all 0.2s;
        }
        .filter-btn:hover { background: #555; }
        .filter-btn.active { border-color: var(--accent); background: #555; }
        .filter-btn.high { border-color: var(--danger); }
        .filter-btn.medium { border-color: var(--warning); }
        .filter-btn.low { border-color: var(--accent); }
        .file-item.hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Godot Performance Analysis</h1>
        <p>Generated on: <span id="gen-date"></span></p>

        <div class="dashboard">
            <div class="card score-card">
                <h3>Overall Health</h3>
                <div id="overall-score" class="score">-</div>
                <p>Based on static analysis rules</p>
            </div>
            <div class="card">
                <h3>Issue Distribution</h3>
                <canvas id="issueChart"></canvas>
            </div>
            <div class="card">
                <h3>Stats</h3>
                <p>Files Scanned: <span id="total-files">0</span></p>
                <p>Total Lines: <span id="total-lines">0</span></p>
                <p>Total Issues: <span id="total-issues">0</span></p>
            </div>
        </div>

        <div class="filter-controls">
            <span style="font-weight: bold;">Filter by Severity:</span>
            <button class="filter-btn" onclick="filterBySeverity('all')" id="filter-all">All Issues</button>
            <button class="filter-btn high" onclick="filterBySeverity('high')" id="filter-high">High Priority</button>
            <button class="filter-btn medium" onclick="filterBySeverity('medium')" id="filter-medium">Medium Priority</button>
            <button class="filter-btn low" onclick="filterBySeverity('low')" id="filter-low">Low Priority</button>
            <span id="filter-status" style="margin-left: auto; color: #aaa;"></span>
        </div>
        
        <div class="filter-controls">
            <span style="font-weight: bold;">Filter by Type:</span>
            <label style="cursor: pointer; padding: 5px 10px; background: #444; border-radius: 4px;">
                <input type="checkbox" id="type-performance" checked onchange="filterByType()"> Performance
            </label>
            <label style="cursor: pointer; padding: 5px 10px; background: #444; border-radius: 4px;">
                <input type="checkbox" id="type-typing" checked onchange="filterByType()"> Typing
            </label>
            <label style="cursor: pointer; padding: 5px 10px; background: #444; border-radius: 4px;">
                <input type="checkbox" id="type-cleanup" checked onchange="filterByType()"> Cleanup
            </label>
            <label style="cursor: pointer; padding: 5px 10px; background: #444; border-radius: 4px;">
                <input type="checkbox" id="type-complexity" checked onchange="filterByType()"> Complexity
            </label>
            <button class="filter-btn" onclick="toggleAllTypes(false)" style="margin-left: 10px;">Hide All</button>
            <button class="filter-btn" onclick="toggleAllTypes(true)">Show All</button>
            <span id="type-status" style="margin-left: auto; color: #aaa;"></span>
        </div>
        
        <h2>Detailed File Analysis</h2>
        <div id="file-list" class="file-list"></div>
    </div>

    <script>
        const data = /*DATA_PLACEHOLDER*/;

        // --- Render Dashboard ---
        document.getElementById('gen-date').textContent = data.generated_at;
        document.getElementById('total-files').textContent = data.total_files;
        document.getElementById('total-lines').textContent = data.total_lines;
        document.getElementById('total-issues').textContent = data.total_issues;
        
        const scoreEl = document.getElementById('overall-score');
        scoreEl.textContent = data.overall_score;
        scoreEl.className = `score ${data.overall_score >= 80 ? 'good' : (data.overall_score >= 50 ? 'medium' : 'bad')}`;

        // Chart with click handler
        const ctx = document.getElementById('issueChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['High Priority', 'Medium Priority', 'Low Priority'],
                datasets: [{
                    data: [data.issues_breakdown.high, data.issues_breakdown.medium, data.issues_breakdown.low],
                    backgroundColor: ['#ff5252', '#ffb142', '#47a6ff'],
                    borderWidth: 0
                }]
            },
            options: { 
                responsive: true, 
                plugins: { 
                    legend: { position: 'bottom', labels: { color: '#bbb' } },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.parsed + ' issues';
                            }
                        }
                    }
                },
                onClick: (event, elements) => {
                    if (elements.length > 0) {
                        const index = elements[0].index;
                        const severity = ['high', 'medium', 'low'][index];
                        filterBySeverity(severity);
                    }
                }
            }
        });

        // --- Render Files ---
        const listEl = document.getElementById('file-list');
        
        // Sort files by score (descending issues / ascending score)
        data.files.sort((a, b) => a.score - b.score);

        data.files.forEach(file => {
            if (file.issues.length === 0 && file.score === 100) return; // Skip perfect files

            const item = document.createElement('div');
            item.className = 'file-item';
            item.dataset.file = file.path;
            
            // Store severity info for filtering
            const severities = new Set(file.issues.map(i => i.severity));
            item.dataset.severities = Array.from(severities).join(',');
            
            const header = document.createElement('div');
            header.className = 'file-header';
            header.innerHTML = `
                <span class="file-name">${file.path}</span>
                <span class="file-score" style="color: ${file.score >= 80 ? '#2cc990' : (file.score >= 50 ? '#ffb142' : '#ff5252')}">
                    Score: ${file.score}
                </span>
            `;
            header.onclick = () => details.classList.toggle('open');
            
            const details = document.createElement('div');
            details.className = 'file-details';
            
            file.issues.forEach(issue => {
                const div = document.createElement('div');
                div.className = `issue ${issue.severity}`;
                div.dataset.severity = issue.severity;
                div.dataset.type = issue.type;
                div.innerHTML = `
                    <div>
                        <span class="issue-line">Line ${issue.line}</span>
                        <span class="issue-type">[${issue.type}]</span>
                        ${issue.message}
                    </div>
                    <div class="code-snippet">${issue.snippet}</div>
                `;
                details.appendChild(div);
            });
            
            item.appendChild(header);
            item.appendChild(details);
            listEl.appendChild(item);
        });
        
        // --- Filter Functionality ---
        let currentFilter = 'all';
        let enabledTypes = new Set(['Performance', 'Typing', 'Cleanup', 'Complexity']);
        
        function filterBySeverity(severity) {
            currentFilter = severity;
            
            // Update button states
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(`filter-${severity}`).classList.add('active');
            
            applyFilters();
        }
        
        function filterByType() {
            // Update enabled types based on checkboxes
            enabledTypes.clear();
            if (document.getElementById('type-performance').checked) enabledTypes.add('Performance');
            if (document.getElementById('type-typing').checked) enabledTypes.add('Typing');
            if (document.getElementById('type-cleanup').checked) enabledTypes.add('Cleanup');
            if (document.getElementById('type-complexity').checked) enabledTypes.add('Complexity');
            
            applyFilters();
        }
        
        function toggleAllTypes(show) {
            document.getElementById('type-performance').checked = show;
            document.getElementById('type-typing').checked = show;
            document.getElementById('type-cleanup').checked = show;
            document.getElementById('type-complexity').checked = show;
            filterByType();
        }
        
        function applyFilters() {
            const fileItems = document.querySelectorAll('.file-item');
            let visibleCount = 0;
            let visibleIssueCount = 0;
            
            fileItems.forEach(item => {
                const details = item.querySelector('.file-details');
                const issues = details.querySelectorAll('.issue');
                let hasVisibleIssue = false;
                
                issues.forEach(issue => {
                    const matchesSeverity = currentFilter === 'all' || issue.dataset.severity === currentFilter;
                    const matchesType = enabledTypes.has(issue.dataset.type);
                    
                    if (matchesSeverity && matchesType) {
                        issue.style.display = '';
                        hasVisibleIssue = true;
                        visibleIssueCount++;
                    } else {
                        issue.style.display = 'none';
                    }
                });
                
                // Hide file if no visible issues
                if (hasVisibleIssue) {
                    item.classList.remove('hidden');
                    visibleCount++;
                } else {
                    item.classList.add('hidden');
                }
            });
            
            // Update status
            const statusEl = document.getElementById('filter-status');
            if (currentFilter === 'all') {
                statusEl.textContent = `Showing ${visibleCount} files with ${visibleIssueCount} issues`;
            } else {
                const severityName = currentFilter.charAt(0).toUpperCase() + currentFilter.slice(1);
                statusEl.textContent = `Showing ${visibleCount} files with ${visibleIssueCount} ${severityName} priority issues`;
            }
            
            // Update type status
            const typeStatusEl = document.getElementById('type-status');
            const typeCount = enabledTypes.size;
            if (typeCount === 4) {
                typeStatusEl.textContent = 'All types shown';
            } else if (typeCount === 0) {
                typeStatusEl.textContent = 'No types selected';
            } else {
                typeStatusEl.textContent = `${typeCount} type(s) shown`;
            }
        }
        
        // Initialize with all issues shown
        filterBySeverity('all');
    </script>
</body>
</html>
"""

class PerformanceAnalyzer:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.issues = []
        self.stats = {
            "total_files": 0,
            "total_lines": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }

    def analyze(self):
        print(f"[*] Starting analysis in {self.root_dir}...")
        files_data = []
        
        for p in self.root_dir.rglob("*.gd"):
            if "addons" in p.parts: continue  # Skip addons
            
            self.stats["total_files"] += 1
            file_result = self.analyze_file(p)
            files_data.append(file_result)
            self.stats["total_lines"] += file_result["lines"]
            
        return self._generate_report_data(files_data)

    def analyze_file(self, path: Path) -> Dict:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        lines = content.split('\n')
        file_issues = []
        
        # State tracking
        in_process_func = False
        process_indent = 0
        
        for i, line in enumerate(lines):
            line_num = i + 1
            stripped = line.strip()
            indent = len(line) - len(line.lstrip())
            
            # Skip comments
            if stripped.startswith('#'): continue
            
            # check function definition
            if stripped.startswith('func'):
                # Reset process state when new func starts
                in_process_func = False
                
                # Check missing type hint on function return
                if '->' not in line and not ':' not in line: # simplistic check
                     pass # Detecting return types robustly requires more complex parsing
                     
                # Detect process loop
                if '_process' in line or '_physics_process' in line:
                    in_process_func = True
                    process_indent = indent
                    continue

            # --- Rules ---
            
            # 1. Expensive calls in process
            if in_process_func and indent > process_indent:
                for patterns in EXPENSIVE_CALLS:
                    if re.search(patterns, line):
                        file_issues.append({
                            "line": line_num,
                            "type": "Performance",
                            "severity": "high",
                            "message": f"Expensive operation detected in process loop: {stripped}",
                            "snippet": self._get_snippet(lines, i, line)
                        })
            
            # 2. Debug prints
            if 'print(' in line and not 'print_debug' in line:
                file_issues.append({
                    "line": line_num,
                    "type": "Cleanup",
                    "severity": "low",
                    "message": "Debug 'print()' call found. Use 'print_debug()' or remove.",
                    "snippet": self._get_snippet(lines, i, line)
                })
                
            # 3. Deep nesting
            if indent >= 16:  # Assuming 4 spaces/tab * 4 levels deep
                 file_issues.append({
                    "line": line_num,
                    "type": "Complexity",
                    "severity": "medium",
                    "message": "Deep nesting detected (4+ levels). Consider refactoring.",
                    "snippet": self._get_snippet(lines, i, line)
                })

            # 4. Missing static typing (Variable)
            # var my_var = ... (bad) vs var my_var: int = ... (good)
            # ignore := inference
            if stripped.startswith('var '):
                if ':' not in line and ':=' not in line:
                     file_issues.append({
                        "line": line_num,
                        "type": "Typing",
                        "severity": "medium",
                        "message": "Missing static type hint on variable. Adding types improves performance.",
                        "snippet": self._get_snippet(lines, i, line)
                    })
            
            # 5. Missing type hints on function parameters/returns (Ollama Recommendation)
            if stripped.startswith('func '):
                # Check for missing return type
                if '->' not in line and not stripped.endswith('void:'):
                    # Allow constructors and special functions without return types
                    if not any(x in line for x in ['_init', '_ready', '_process', '_physics_process', '_input']):
                        file_issues.append({
                            "line": line_num,
                            "type": "Typing",
                            "severity": "medium",
                            "message": "Missing return type hint on function. Use '-> Type:' for better performance.",
                            "snippet": self._get_snippet(lines, i, line)
                        })
                
                # Check for untyped parameters
                if '(' in line and ')' in line:
                    params_section = line[line.index('('):line.index(')')+1]
                    # Simple check: if there's a parameter without ':'
                    if ',' in params_section or ('(' in params_section and ')' in params_section):
                        # Has parameters, check if typed
                        params = params_section.strip('()').split(',')
                        for param in params:
                            param = param.strip()
                            if param and ':' not in param and '=' not in param and param != '':
                                file_issues.append({
                                    "line": line_num,
                                    "type": "Typing",
                                    "severity": "medium",
                                    "message": f"Missing type hint on parameter. Use 'param: Type' syntax.",
                                    "snippet": self._get_snippet(lines, i, line)
                                })
                                break  # Only report once per function
            
            # 6. Costly memory operations in loops (Ollama Recommendation)
            # Detect array/dictionary allocations inside loops
            if any(keyword in stripped for keyword in ['for ', 'while ']):
                # Mark that we're in a loop
                pass
            
            # Check for array/dict creation patterns
            if in_process_func or any(keyword in content[max(0, i-10):i] for keyword in ['for ', 'while ']):
                if re.search(r'\[\s*\]|\{\s*\}|Array\.new\(\)|Dictionary\.new\(\)', line):
                    file_issues.append({
                        "line": line_num,
                        "type": "Performance",
                        "severity": "high",
                        "message": "Memory allocation detected in hot path. Consider pre-allocating or moving outside loop.",
                        "snippet": self._get_snippet(lines, i, line)
                    })
            
            # 7. Redundant computations (Ollama Recommendation)
            # Detect repeated expensive calls that could be cached
            if in_process_func and indent > process_indent:
                # Look for repeated method calls on same object
                if '.get_' in line or '.calculate_' in line or '.find_' in line:
                    file_issues.append({
                        "line": line_num,
                        "type": "Performance",
                        "severity": "medium",
                        "message": "Potentially redundant computation in process loop. Consider caching result.",
                        "snippet": self._get_snippet(lines, i, line)
                    })

        # Severity-weighted scoring
        # High severity issues are more impactful than medium/low
        high_count = len([i for i in file_issues if i['severity'] == 'high'])
        medium_count = len([i for i in file_issues if i['severity'] == 'medium'])
        low_count = len([i for i in file_issues if i['severity'] == 'low'])
        
        # Weighted penalty: high=15, medium=2, low=0.5
        # This ensures high-severity issues are heavily penalized
        # while type hints (medium) don't automatically cause 0 scores
        penalty = (high_count * 15) + (medium_count * 2) + (low_count * 0.5)
        score = max(0, 100 - penalty)
        
        return {
            "path": str(path.relative_to(self.root_dir)),
            "score": score,
            "issues": file_issues,
            "lines": len(lines)
        }

    def _get_snippet(self, lines, index, current_line):
        start = max(0, index - 1)
        end = min(len(lines), index + 2)
        snippet = ""
        for i in range(start, end):
            prefix = "> " if i == index else "  "
            snippet += f"{prefix}{lines[i]}\n"
        return snippet

    def _generate_report_data(self, files: List[Dict]) -> Dict:
        total_issues = sum(len(f['issues']) for f in files)
        
        high = sum(len([i for i in f['issues'] if i['severity'] == 'high']) for f in files)
        medium = sum(len([i for i in f['issues'] if i['severity'] == 'medium']) for f in files)
        low = sum(len([i for i in f['issues'] if i['severity'] == 'low']) for f in files)
        
        # Calculate overall project health
        avg_score = sum(f['score'] for f in files) / len(files) if files else 100
        
        return {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "overall_score": int(avg_score),
            "total_files": self.stats['total_files'],
            "total_lines": self.stats['total_lines'],
            "total_issues": total_issues,
            "issues_breakdown": { "high": high, "medium": medium, "low": low },
            "files": files
        }

def main():
    try:
        analyzer = PerformanceAnalyzer(PROJECT_ROOT)
        data = analyzer.analyze()
        
        # Inject data into HTML
        json_data = json.dumps(data)
        html_content = HTML_TEMPLATE.replace("/*DATA_PLACEHOLDER*/", json_data)
        
        # Save timestamped report
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Create/update latest link (copy for Windows compatibility)
        import shutil
        try:
            if os.path.exists(LATEST_LINK):
                os.remove(LATEST_LINK)
            shutil.copy2(OUTPUT_FILE, LATEST_LINK)
        except Exception as e:
            print(f"Warning: Could not create latest link: {e}")
            
        print("\n" + "="*60)
        print(f"Analysis Complete!")
        print(f"Files Scanned: {data['total_files']}")
        print(f"Total Issues: {data['total_issues']}")
        print(f"Report saved to: {os.path.abspath(OUTPUT_FILE)}")
        print(f"Latest copy at: {os.path.abspath(LATEST_LINK)}")
        print(f"All reports in: {os.path.abspath(REPORTS_DIR)}")
        print("="*60)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
