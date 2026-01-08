import json
import re

# Read the latest report
with open('reports/performance_report_2026-01-08_10-20-57.html', encoding='utf-8') as f:
    content = f.read()

# Extract JSON data
match = re.search(r'const data = ({.*?});', content, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    
    # Find test_gravity_manager file
    test_file = None
    for f in data['files']:
        if 'test_gravity_manager' in f['path']:
            test_file = f
            break
    
    if test_file:
        print(f"File: {test_file['path']}")
        print(f"Score: {test_file['score']}")
        print(f"Total issues: {len(test_file['issues'])}")
        
        # Count by severity
        severity_counts = {'high': 0, 'medium': 0, 'low': 0}
        for issue in test_file['issues']:
            severity_counts[issue['severity']] += 1
        
        print(f"\nBreakdown:")
        print(f"  High: {severity_counts['high']}")
        print(f"  Medium: {severity_counts['medium']}")
        print(f"  Low: {severity_counts['low']}")
        
        # Calculate expected score
        penalty = (severity_counts['high'] * 10) + (severity_counts['medium'] * 3) + (severity_counts['low'] * 1)
        expected_score = max(0, 100 - penalty)
        print(f"\nExpected score: {expected_score}")
        print(f"Actual score: {test_file['score']}")
        
        if expected_score != test_file['score']:
            print(f"\n❌ MISMATCH! Score should be {expected_score}, not {test_file['score']}")
        else:
            print(f"\n✅ Score is correct!")
