#!/usr/bin/env python3
"""
Title Scorer - Evaluate book titles for Gen Z viral potential

Scores titles based on:
- Length optimization (40-80 chars ideal)
- Power word presence (urgency, rebellion, achievement)
- Emotional triggers (curiosity, FOMO, challenge)
- Numbers/timeframes (specificity)
- Searchability (keywords)
- Gen Z language patterns

Usage:
    python title-scorer.py "Your Book Title Here"
    python title-scorer.py --batch titles.txt
"""

import sys
import re
from typing import Dict, List, Tuple

# Power word categories
POWER_WORDS = {
    'urgency': ['speedrun', 'glitch', 'hack', 'now', 'today', 'before', 'late', 'cheat'],
    'rebellion': ['wrong', 'broke', 'outdated', 'secret', 'hidden', 'unconventional', 'rebellious'],
    'achievement': ['level up', 'unlock', 'boss', 'playbook', 'blueprint', 'winning', 'dominating'],
    'relatable': ['real talk', 'honest', 'no bs', 'actually', 'worked', 'simple', 'easy'],
    'timeframe': ['days', 'hours', 'weeks', 'months', 'year', '24', '48', '90', '365']
}

# Emotional triggers
EMOTIONAL_PATTERNS = {
    'curiosity': [r'\bwhy\b', r'\bhow\b', r'\bwhat\b', r'\bsecret\b', r'\bhidden\b', r'no one tells'],
    'fomo': [r'\bbefore\b', r'\bnow\b', r'\btoday\b', r'\bmissing\b', r'\bglitch\b'],
    'challenge': [r'\bspeedrun\b', r'\bchallenge\b', r'\btest\b', r'\bprove\b'],
    'hope': [r'\bsuccess\b', r'\bwin\b', r'\brich\b', r'\bboss\b', r'\bfree\b']
}

# Gen Z linguistic markers
GENZ_PATTERNS = [
    r'\bspeedrun\b', r'\bglitch\b', r'\bhack\b', r'\bno cap\b', 
    r'\breal talk\b', r'\bfr\b', r'\bvibe\b', r'\bslaps\b'
]

def score_title(title: str) -> Dict:
    """
    Score a single title across multiple dimensions
    
    Returns dict with scores and recommendations
    """
    title_lower = title.lower()
    scores = {}
    recommendations = []
    
    # 1. Length Score (0-20 points)
    length = len(title)
    if 40 <= length <= 80:
        scores['length'] = 20
    elif 30 <= length < 40 or 80 < length <= 100:
        scores['length'] = 15
        recommendations.append("Length okay but not ideal. Aim for 40-80 characters.")
    elif 20 <= length < 30 or 100 < length <= 120:
        scores['length'] = 10
        recommendations.append("Length suboptimal. Target 40-80 characters for best engagement.")
    else:
        scores['length'] = 5
        recommendations.append(f"Length critical: {length} chars. Ideal is 40-80 for social sharing.")
    
    # 2. Power Words Score (0-25 points)
    power_word_count = 0
    found_categories = []
    
    for category, words in POWER_WORDS.items():
        for word in words:
            if word in title_lower:
                power_word_count += 1
                if category not in found_categories:
                    found_categories.append(category)
    
    scores['power_words'] = min(power_word_count * 5, 25)
    if scores['power_words'] < 10:
        recommendations.append("Add more power words (speedrun, hack, secret, unlock, etc.)")
    
    # 3. Emotional Triggers (0-20 points)
    emotional_hits = []
    for emotion, patterns in EMOTIONAL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, title_lower):
                emotional_hits.append(emotion)
                break
    
    scores['emotional'] = len(set(emotional_hits)) * 5
    if scores['emotional'] < 10:
        recommendations.append("Add emotional triggers: curiosity (Why/How), FOMO (Before/Now), or challenge")
    
    # 4. Numbers/Specificity (0-15 points)
    number_pattern = r'\b\d+\b'
    numbers = re.findall(number_pattern, title)
    
    if numbers:
        scores['specificity'] = 15
    elif any(word in title_lower for word in ['first', 'last', 'ultimate', 'complete']):
        scores['specificity'] = 10
        recommendations.append("Good qualifier words, but actual numbers work better (7, 90, $10K)")
    else:
        scores['specificity'] = 5
        recommendations.append("Add numbers for specificity: '$10K', '90 Days', '7 Secrets'")
    
    # 5. Gen Z Language (0-10 points)
    genz_hits = sum(1 for pattern in GENZ_PATTERNS if re.search(pattern, title_lower))
    scores['genz_lang'] = min(genz_hits * 5, 10)
    
    if scores['genz_lang'] < 5:
        recommendations.append("Use more Gen Z language: speedrun, glitch, hack, real talk")
    
    # 6. Searchability (0-10 points)
    # Check for common search keywords
    search_keywords = ['how to', 'guide', 'tips', 'strategies', 'playbook', 'blueprint']
    search_hits = sum(1 for kw in search_keywords if kw in title_lower)
    
    scores['searchability'] = min(search_hits * 5, 10)
    if scores['searchability'] < 5:
        recommendations.append("Consider adding searchable terms: 'Guide', 'Playbook', 'Blueprint'")
    
    # Calculate total score
    total = sum(scores.values())
    
    # Grade assignment
    if total >= 85:
        grade = 'A'
        verdict = "🔥 Viral potential - Strong title!"
    elif total >= 70:
        grade = 'B'
        verdict = "✅ Good title - Minor tweaks recommended"
    elif total >= 55:
        grade = 'C'
        verdict = "⚠️ Needs work - Follow recommendations"
    else:
        grade = 'D'
        verdict = "❌ Weak title - Major revision needed"
    
    return {
        'title': title,
        'total_score': total,
        'grade': grade,
        'verdict': verdict,
        'scores': scores,
        'recommendations': recommendations,
        'power_word_categories': found_categories,
        'emotional_triggers': list(set(emotional_hits)),
        'numbers_found': numbers
    }


def print_results(result: Dict):
    """Pretty print scoring results"""
    print("\n" + "="*70)
    print(f"TITLE: {result['title']}")
    print("="*70)
    print(f"\n📊 TOTAL SCORE: {result['total_score']}/100")
    print(f"🎯 GRADE: {result['grade']}")
    print(f"💬 {result['verdict']}\n")
    
    print("DETAILED BREAKDOWN:")
    print("-" * 70)
    print(f"Length ({len(result['title'])} chars)     : {result['scores']['length']}/20")
    print(f"Power Words                : {result['scores']['power_words']}/25")
    print(f"Emotional Triggers         : {result['scores']['emotional']}/20")
    print(f"Specificity (Numbers)      : {result['scores']['specificity']}/15")
    print(f"Gen Z Language             : {result['scores']['genz_lang']}/10")
    print(f"Searchability              : {result['scores']['searchability']}/10")
    
    if result['power_word_categories']:
        print(f"\n✅ Power word types found: {', '.join(result['power_word_categories'])}")
    
    if result['emotional_triggers']:
        print(f"✅ Emotional triggers: {', '.join(result['emotional_triggers'])}")
    
    if result['numbers_found']:
        print(f"✅ Numbers used: {', '.join(result['numbers_found'])}")
    
    if result['recommendations']:
        print("\n💡 RECOMMENDATIONS:")
        print("-" * 70)
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"{i}. {rec}")
    
    print("\n" + "="*70 + "\n")


def batch_score(filename: str):
    """Score multiple titles from a file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            titles = [line.strip() for line in f if line.strip()]
        
        print(f"\n📚 Scoring {len(titles)} titles from {filename}\n")
        
        results = []
        for title in titles:
            result = score_title(title)
            results.append(result)
        
        # Sort by score
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        # Print summary
        print("\n" + "="*70)
        print("BATCH RESULTS SUMMARY (Ranked by Score)")
        print("="*70 + "\n")
        
        for i, result in enumerate(results, 1):
            print(f"{i}. [{result['grade']} - {result['total_score']}/100] {result['title']}")
        
        # Print detailed results
        for result in results:
            print_results(result)
        
        # Best title recommendation
        best = results[0]
        print("🏆 TOP RECOMMENDATION:")
        print(f"   '{best['title']}' (Score: {best['total_score']}/100)")
        
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nExamples:")
        print('  python title-scorer.py "Side Hustle Speedrun: Broke to Boss in 90 Days"')
        print('  python title-scorer.py --batch titles.txt')
        sys.exit(1)
    
    if sys.argv[1] == '--batch':
        if len(sys.argv) < 3:
            print("❌ Error: Please provide filename for batch mode")
            print('Usage: python title-scorer.py --batch titles.txt')
            sys.exit(1)
        batch_score(sys.argv[2])
    else:
        title = ' '.join(sys.argv[1:])
        result = score_title(title)
        print_results(result)


if __name__ == '__main__':
    main()
