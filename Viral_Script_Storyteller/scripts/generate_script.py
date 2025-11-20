#!/usr/bin/env python3
"""
Viral Script Generator
Generates video script scaffolds based on format and topic
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

# Script templates with placeholders
TEMPLATES = {
    "short": {
        "duration": "15-30s",
        "structure": [
            {"section": "HOOK", "time": "0-3s", "placeholder": "[Insert shock/curiosity hook]"},
            {"section": "VALUE", "time": "3-20s", "placeholder": "[Insert main insight with visual]"},
            {"section": "CTA", "time": "20-30s", "placeholder": "[Insert specific action]"}
        ]
    },
    "tutorial": {
        "duration": "30-60s",
        "structure": [
            {"section": "HOOK", "time": "0-5s", "placeholder": "[Insert problem-solution hook]"},
            {"section": "STEP 1", "time": "5-20s", "placeholder": "[First action + visual]"},
            {"section": "STEP 2", "time": "20-35s", "placeholder": "[Second action + visual]"},
            {"section": "STEP 3", "time": "35-50s", "placeholder": "[Final action + result]"},
            {"section": "CTA", "time": "50-60s", "placeholder": "[Follow/save/comment CTA]"}
        ]
    },
    "explainer": {
        "duration": "30-60s",
        "structure": [
            {"section": "HOOK", "time": "0-5s", "placeholder": "[Curiosity gap opener]"},
            {"section": "ANALOGY", "time": "5-20s", "placeholder": "[Everyday comparison]"},
            {"section": "TECHNICAL", "time": "20-40s", "placeholder": "[How it actually works]"},
            {"section": "RESULT", "time": "40-55s", "placeholder": "[Why it matters]"},
            {"section": "CTA", "time": "55-60s", "placeholder": "[Engage action]"}
        ]
    },
    "transformation": {
        "duration": "45-60s",
        "structure": [
            {"section": "HOOK", "time": "0-5s", "placeholder": "[Before state shock]"},
            {"section": "PROBLEM", "time": "5-15s", "placeholder": "[Pain point amplification]"},
            {"section": "DISCOVERY", "time": "15-30s", "placeholder": "[Solution reveal]"},
            {"section": "PROCESS", "time": "30-50s", "placeholder": "[How you did it]"},
            {"section": "RESULT", "time": "50-55s", "placeholder": "[After state proof]"},
            {"section": "CTA", "time": "55-60s", "placeholder": "[Invitation to follow journey]"}
        ]
    }
}

PLATFORM_SPECS = {
    "tiktok": {"max_duration": 60, "optimal": "15-30s", "aspect": "9:16", "cta": "comment/duet"},
    "instagram": {"max_duration": 90, "optimal": "30-45s", "aspect": "9:16", "cta": "save/share"},
    "youtube": {"max_duration": 60, "optimal": "30-60s", "aspect": "9:16", "cta": "subscribe"},
    "linkedin": {"max_duration": 600, "optimal": "45-90s", "aspect": "1:1/16:9", "cta": "repost/follow"}
}

def generate_script(topic, format_type, platform, output_path):
    """Generate script scaffold with metadata"""
    
    if format_type not in TEMPLATES:
        print(f"❌ Unknown format: {format_type}")
        print(f"✓ Available: {', '.join(TEMPLATES.keys())}")
        return
    
    template = TEMPLATES[format_type]
    platform_info = PLATFORM_SPECS.get(platform, {})
    
    # Build script
    script = {
        "metadata": {
            "topic": topic,
            "format": format_type,
            "platform": platform,
            "target_duration": template["duration"],
            "aspect_ratio": platform_info.get("aspect", "9:16"),
            "generated_at": datetime.now().isoformat(),
        },
        "script_structure": []
    }
    
    # Add sections
    for section in template["structure"]:
        script["script_structure"].append({
            "section": section["section"],
            "timing": section["time"],
            "script_text": section["placeholder"],
            "visual_notes": "[Describe visual here]",
            "shot_type": "[Wide/Medium/Close-up]"
        })
    
    # Add production notes
    script["production_notes"] = {
        "hook_quality": "❗ First 3s determine success",
        "visual_pace": "Change visual every 3-5 seconds",
        "text_overlays": "Use power words: FREE, HACK, MISTAKE, SECRET",
        "cta_type": platform_info.get("cta", "engage"),
        "music_vibe": "[Upbeat/Dramatic/Chill]"
    }
    
    # Save to file
    output_file = Path(output_path) / f"{format_type}_{platform}_{topic.replace(' ', '_')}.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(script, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Script scaffold generated: {output_file}")
    print(f"📊 Format: {format_type} | Platform: {platform}")
    print(f"⏱️  Target duration: {template['duration']}")
    print(f"\n📝 Next steps:")
    print(f"   1. Open {output_file.name}")
    print(f"   2. Replace placeholders with actual script")
    print(f"   3. Add visual descriptions for editor")
    print(f"   4. Test read-aloud timing")
    
    return output_file

def print_available_formats():
    """Display all available formats with descriptions"""
    print("\n📚 Available Script Formats:\n")
    for fmt, details in TEMPLATES.items():
        print(f"  {fmt.upper()}")
        print(f"    Duration: {details['duration']}")
        print(f"    Sections: {len(details['structure'])}")
        print(f"    Structure: {' → '.join([s['section'] for s in details['structure']])}")
        print()

def main():
    parser = argparse.ArgumentParser(
        description="Generate viral video script scaffolds",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_script.py "Docker for beginners" tutorial tiktok
  python generate_script.py "API optimization" short instagram
  python generate_script.py "How RAG works" explainer youtube
  python generate_script.py --list
        """
    )
    
    parser.add_argument("topic", nargs="?", help="Video topic/title")
    parser.add_argument("format", nargs="?", choices=TEMPLATES.keys(), 
                       help="Script format type")
    parser.add_argument("platform", nargs="?", choices=PLATFORM_SPECS.keys(),
                       help="Target platform")
    parser.add_argument("-o", "--output", default="./output",
                       help="Output directory (default: ./output)")
    parser.add_argument("--list", action="store_true",
                       help="List available formats")
    
    args = parser.parse_args()
    
    if args.list:
        print_available_formats()
        return
    
    if not all([args.topic, args.format, args.platform]):
        parser.print_help()
        print("\n💡 Use --list to see available formats")
        return
    
    generate_script(args.topic, args.format, args.platform, args.output)

if __name__ == "__main__":
    main()
