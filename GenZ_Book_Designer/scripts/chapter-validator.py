#!/usr/bin/env python3
"""
Chapter Validator - Check Gen Z book chapters for optimal engagement

Validates:
- Sub-chapter word counts (target: 800-1500 words)
- Pit stop placement (should be every sub-chapter)
- Hook presence (chapters must start with hooks)
- Flow/pacing (variety in pit stop types)
- Naming conventions (no boring "Chapter 1, 2, 3")

Usage:
    python chapter-validator.py manuscript.txt
    python chapter-validator.py --chapter "Chapter 1" chapter1.txt
    python chapter-validator.py --json output.json manuscript.txt
"""

import sys
import re
import json
import argparse
from typing import Dict, List, Tuple

# Validation criteria
WORD_COUNT_OPTIMAL = (800, 1500)
WORD_COUNT_ACCEPTABLE = (500, 2000)
PIT_STOP_INTERVAL = 1  # One pit stop per sub-chapter

# Hook indicators (opening patterns)
HOOK_PATTERNS = [
    r'^".*"',  # Starts with quote
    r'^\w+\s+\d+,\s+\d{4}',  # Starts with date (Last Tuesday, May 5, 2024)
    r'^(What|Why|How|When|Where)',  # Starts with question word
    r'^\$[\d,]+',  # Starts with money amount
    r'^I (lost|made|learned|discovered|failed)',  # Personal story opening
    r'^Here\'s the thing',  # Conversational hook
    r'^Nobody tells you',  # Secret reveal hook
]

# Boring chapter name patterns to flag
BORING_PATTERNS = [
    r'^Chapter\s+\d+',
    r'^Part\s+\d+',
    r'^Section\s+\d+',
    r'^Introduction',
    r'^Conclusion',
]

def parse_manuscript(content: str) -> List[Dict]:
    """
    Parse manuscript into structured chapters
    
    Expected format:
        # Chapter Name
        
        ## Sub-chapter 1
        Content...
        
        ### PIT STOP: Name
        Pit stop content...
        
        ## Sub-chapter 2
        Content...
    """
    chapters = []
    current_chapter = None
    current_subchapter = None
    current_pitstop = None
    
    lines = content.split('\n')
    
    for line in lines:
        # Chapter header (# Chapter Name)
        if line.startswith('# ') and not line.startswith('## '):
            if current_chapter:
                chapters.append(current_chapter)
            
            current_chapter = {
                'name': line[2:].strip(),
                'subchapters': [],
                'line_number': len(chapters) + 1
            }
            current_subchapter = None
            current_pitstop = None
        
        # Sub-chapter header (## Sub-chapter Name)
        elif line.startswith('## ') and not line.startswith('### '):
            if current_chapter:
                if current_subchapter:
                    current_chapter['subchapters'].append(current_subchapter)
                
                current_subchapter = {
                    'name': line[3:].strip(),
                    'content': '',
                    'has_pitstop': False,
                    'pitstop': None
                }
                current_pitstop = None
        
        # Pit stop header (### PIT STOP: Name)
        elif line.startswith('### PIT STOP:'):
            if current_subchapter:
                current_subchapter['has_pitstop'] = True
                current_pitstop = {
                    'name': line[13:].strip(),
                    'content': ''
                }
                current_subchapter['pitstop'] = current_pitstop
        
        # Content
        else:
            if current_pitstop:
                current_pitstop['content'] += line + '\n'
            elif current_subchapter:
                current_subchapter['content'] += line + '\n'
    
    # Append last chapter
    if current_chapter:
        if current_subchapter:
            current_chapter['subchapters'].append(current_subchapter)
        chapters.append(current_chapter)
    
    return chapters


def count_words(text: str) -> int:
    """Count words in text, excluding markdown formatting"""
    # Remove markdown headers
    text = re.sub(r'^#+\s+.*$', '', text, flags=re.MULTILINE)
    # Remove markdown formatting
    text = re.sub(r'[*_`]', '', text)
    # Count words
    words = text.split()
    return len(words)


def check_hook(content: str) -> Tuple[bool, str]:
    """Check if content starts with a hook"""
    # Get first paragraph
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    if not paragraphs:
        return False, "No content found"
    
    first_para = paragraphs[0]
    
    for pattern in HOOK_PATTERNS:
        if re.search(pattern, first_para, re.IGNORECASE):
            return True, "Good hook detected"
    
    return False, "No clear hook - consider starting with story, question, or stat"


def check_chapter_name(name: str) -> Tuple[bool, str]:
    """Check if chapter name follows Gen Z best practices"""
    for pattern in BORING_PATTERNS:
        if re.search(pattern, name, re.IGNORECASE):
            return False, f"Boring pattern detected: '{name}'"
    
    # Check length
    if len(name) > 80:
        return False, f"Too long ({len(name)} chars) - keep under 80"
    
    if len(name) < 10:
        return False, f"Too short ({len(name)} chars) - aim for 20-60"
    
    return True, "Good chapter name"


def validate_chapter(chapter: Dict) -> Dict:
    """Validate a single chapter structure"""
    issues = []
    warnings = []
    stats = {
        'total_words': 0,
        'subchapters': len(chapter['subchapters']),
        'pitstops': 0,
        'avg_words_per_sub': 0
    }
    
    # Check chapter name
    name_ok, name_msg = check_chapter_name(chapter['name'])
    if not name_ok:
        issues.append(f"Chapter name: {name_msg}")
    
    # Validate sub-chapters
    for i, sub in enumerate(chapter['subchapters'], 1):
        word_count = count_words(sub['content'])
        stats['total_words'] += word_count
        
        # Word count check
        if word_count < WORD_COUNT_ACCEPTABLE[0]:
            issues.append(f"Sub-chapter {i} too short: {word_count} words (min {WORD_COUNT_ACCEPTABLE[0]})")
        elif word_count > WORD_COUNT_ACCEPTABLE[1]:
            warnings.append(f"Sub-chapter {i} too long: {word_count} words (max {WORD_COUNT_ACCEPTABLE[1]})")
        elif word_count < WORD_COUNT_OPTIMAL[0] or word_count > WORD_COUNT_OPTIMAL[1]:
            warnings.append(f"Sub-chapter {i} word count suboptimal: {word_count} (target {WORD_COUNT_OPTIMAL[0]}-{WORD_COUNT_OPTIMAL[1]})")
        
        # Hook check (only for first sub-chapter)
        if i == 1:
            has_hook, hook_msg = check_hook(sub['content'])
            if not has_hook:
                warnings.append(f"Chapter opening: {hook_msg}")
        
        # Pit stop check
        if sub['has_pitstop']:
            stats['pitstops'] += 1
        else:
            issues.append(f"Sub-chapter {i} missing pit stop")
    
    # Calculate average
    if stats['subchapters'] > 0:
        stats['avg_words_per_sub'] = stats['total_words'] // stats['subchapters']
    
    # Check pit stop frequency
    if stats['pitstops'] < stats['subchapters']:
        issues.append(f"Only {stats['pitstops']}/{stats['subchapters']} sub-chapters have pit stops")
    
    return {
        'chapter_name': chapter['name'],
        'stats': stats,
        'issues': issues,
        'warnings': warnings,
        'status': 'PASS' if len(issues) == 0 else 'FAIL'
    }


def print_validation_results(results: List[Dict]):
    """Pretty print validation results"""
    total_issues = sum(len(r['issues']) for r in results)
    total_warnings = sum(len(r['warnings']) for r in results)
    passed = sum(1 for r in results if r['status'] == 'PASS')
    
    print("\n" + "="*70)
    print("MANUSCRIPT VALIDATION RESULTS")
    print("="*70)
    print(f"\nChapters analyzed: {len(results)}")
    print(f"Status: {passed}/{len(results)} PASSED")
    print(f"Issues: {total_issues} critical")
    print(f"Warnings: {total_warnings} minor")
    print("\n" + "="*70 + "\n")
    
    for result in results:
        status_icon = "✅" if result['status'] == 'PASS' else "❌"
        print(f"{status_icon} {result['chapter_name']}")
        print("-" * 70)
        
        # Stats
        stats = result['stats']
        print(f"   Total words: {stats['total_words']}")
        print(f"   Sub-chapters: {stats['subchapters']}")
        print(f"   Pit stops: {stats['pitstops']}")
        print(f"   Avg words/sub: {stats['avg_words_per_sub']}")
        
        # Issues
        if result['issues']:
            print(f"\n   ❌ CRITICAL ISSUES ({len(result['issues'])}):")
            for issue in result['issues']:
                print(f"      • {issue}")
        
        # Warnings
        if result['warnings']:
            print(f"\n   ⚠️  WARNINGS ({len(result['warnings'])}):")
            for warning in result['warnings']:
                print(f"      • {warning}")
        
        print()
    
    # Overall recommendation
    print("="*70)
    if total_issues == 0:
        print("🎉 READY TO PUBLISH")
        print("All chapters meet Gen Z engagement criteria!")
    elif total_issues <= 3:
        print("⚠️  MINOR FIXES NEEDED")
        print("Address critical issues before publishing.")
    else:
        print("🔧 MAJOR REVISION REQUIRED")
        print("Multiple chapters need structural improvements.")
    print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(description='Validate Gen Z book manuscript structure')
    parser.add_argument('file', type=str, help='Manuscript file to validate')
    parser.add_argument('--chapter', type=str, help='Validate specific chapter only')
    parser.add_argument('--json', type=str, help='Output results as JSON to file')
    
    args = parser.parse_args()
    
    # Read manuscript
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File '{args.file}' not found")
        sys.exit(1)
    
    # Parse manuscript
    chapters = parse_manuscript(content)
    
    if not chapters:
        print("❌ No chapters found. Ensure manuscript uses proper markdown headers:")
        print("   # Chapter Name")
        print("   ## Sub-chapter Name")
        print("   ### PIT STOP: Name")
        sys.exit(1)
    
    # Filter by specific chapter if requested
    if args.chapter:
        chapters = [c for c in chapters if args.chapter.lower() in c['name'].lower()]
        if not chapters:
            print(f"❌ Chapter '{args.chapter}' not found")
            sys.exit(1)
    
    # Validate all chapters
    results = [validate_chapter(chapter) for chapter in chapters]
    
    # Output results
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"✅ Results saved to {args.json}")
    else:
        print_validation_results(results)


if __name__ == '__main__':
    main()
