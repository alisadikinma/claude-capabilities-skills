#!/usr/bin/env python3
"""
Performance Analyzer - Web_Architect_Pro
Analyze bundle sizes and provide optimization recommendations

Usage:
    python performance_analyzer.py analyze ./build
    python performance_analyzer.py compare ./build-before ./build-after
"""

import sys
import gzip
from pathlib import Path
from collections import defaultdict

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def format_size(size_bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def get_size_color(size_kb: float) -> str:
    if size_kb < 50:
        return Colors.GREEN
    elif size_kb < 150:
        return Colors.YELLOW
    return Colors.RED

def analyze_directory(dir_path: Path):
    results = defaultdict(list)
    
    for file_path in dir_path.rglob('*'):
        if file_path.is_file():
            ext = file_path.suffix.lower()
            
            if ext in ['.map', '.txt', '.md']:
                continue
            
            size = file_path.stat().st_size
            gzip_size = 0
            
            if ext in ['.js', '.css', '.html', '.json']:
                with open(file_path, 'rb') as f:
                    gzip_size = len(gzip.compress(f.read()))
            
            results[ext].append({
                'path': str(file_path.relative_to(dir_path)),
                'size': size,
                'gzip_size': gzip_size
            })
    
    return results

def print_analysis(results, title="Build Analysis"):
    print(f"\n{Colors.BLUE}{title}{Colors.RESET}\n")
    
    total_size = sum(sum(f['size'] for f in files) for files in results.values())
    total_gzip = sum(sum(f['gzip_size'] for f in files) for files in results.values())
    
    print(f"Total Size:    {format_size(total_size)}")
    print(f"Total Gzipped: {format_size(total_gzip)}")
    if total_gzip > 0:
        print(f"Compression:   {(1 - total_gzip / total_size) * 100:.1f}%\n")
    
    for ext in sorted(results.keys()):
        files = sorted(results[ext], key=lambda x: x['size'], reverse=True)
        type_total = sum(f['size'] for f in files)
        type_gzip = sum(f['gzip_size'] for f in files)
        
        print(f"{Colors.BLUE}{ext.upper() or 'NO EXT'} ({len(files)}):{Colors.RESET}")
        print(f"  Total: {format_size(type_total)}", end='')
        if type_gzip > 0:
            print(f" → {format_size(type_gzip)}")
        else:
            print()
        
        for file in files[:5]:
            size_kb = file['size'] / 1024
            color = get_size_color(size_kb)
            gzip_info = f" → {format_size(file['gzip_size'])}" if file['gzip_size'] > 0 else ""
            print(f"  {color}▪{Colors.RESET} {file['path']:50} {format_size(file['size'])}{gzip_info}")
        
        if len(files) > 5:
            print(f"  ... {len(files) - 5} more\n")
        else:
            print()

def get_recommendations(results):
    recs = []
    
    js_files = results.get('.js', [])
    large_js = [f for f in js_files if f['size'] > 200 * 1024]
    
    if large_js:
        recs.append(f"🔴 {len(large_js)} large JS files (>200KB). Consider code splitting.")
    
    css_files = results.get('.css', [])
    large_css = [f for f in css_files if f['size'] > 100 * 1024]
    
    if large_css:
        recs.append(f"🟡 {len(large_css)} large CSS files (>100KB). Remove unused styles.")
    
    total_js = sum(f['size'] for f in js_files)
    if total_js > 500 * 1024:
        recs.append(f"🔴 Total JS: {format_size(total_js)}. Review dependencies.")
    
    return recs

def analyze_command(dir_path: str):
    path = Path(dir_path)
    if not path.exists():
        print(f"{Colors.RED}Directory not found: {dir_path}{Colors.RESET}")
        sys.exit(1)
    
    results = analyze_directory(path)
    print_analysis(results)
    
    recs = get_recommendations(results)
    if recs:
        print(f"\n{Colors.BLUE}💡 Recommendations:{Colors.RESET}\n")
        for rec in recs:
            print(f"  {rec}")
    else:
        print(f"\n{Colors.GREEN}✅ No major issues{Colors.RESET}")

def compare_command(before_path: str, after_path: str):
    before = Path(before_path)
    after = Path(after_path)
    
    if not before.exists() or not after.exists():
        print(f"{Colors.RED}Directory not found{Colors.RESET}")
        sys.exit(1)
    
    before_results = analyze_directory(before)
    after_results = analyze_directory(after)
    
    before_total = sum(sum(f['size'] for f in files) for files in before_results.values())
    after_total = sum(sum(f['size'] for f in files) for files in after_results.values())
    
    diff = after_total - before_total
    
    print(f"\n{Colors.BLUE}Comparison:{Colors.RESET}\n")
    print(f"Before: {format_size(before_total)}")
    print(f"After:  {format_size(after_total)}")
    
    if diff > 0:
        print(f"Change: {Colors.RED}+{format_size(diff)}{Colors.RESET}")
    else:
        print(f"Change: {Colors.GREEN}{format_size(diff)}{Colors.RESET}")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python performance_analyzer.py analyze <dir>")
        print("  python performance_analyzer.py compare <before> <after>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'analyze' and len(sys.argv) >= 3:
        analyze_command(sys.argv[2])
    elif command == 'compare' and len(sys.argv) >= 4:
        compare_command(sys.argv[2], sys.argv[3])
    else:
        print(f"{Colors.RED}Invalid command{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
