#!/usr/bin/env python3
"""
Hook Analyzer - Validate viral hook effectiveness
Analyzes video hooks for attention-grabbing power using proven metrics
"""

import re
import sys
from typing import Dict, List, Tuple

# Power words that increase hook effectiveness
POWER_WORDS = {
    'shock': ['wrong', 'mistake', 'fail', 'broke', 'disaster', 'hidden', 'secret', 'truth'],
    'curiosity': ['why', 'how', 'what', 'discover', 'reveal', 'nobody', 'never'],
    'urgency': ['now', 'today', 'immediately', 'quick', 'fast', 'instant'],
    'transformation': ['from', 'to', 'became', 'changed', 'transformed', '10x', 'double'],
    'negation': ['stop', 'don\'t', 'never', 'avoid', 'quit', 'forget'],
    'authority': ['expert', 'proven', 'tested', 'professional', 'advanced', 'secret']
}

# Hook patterns (regex)
HOOK_PATTERNS = {
    'question': r'\?',
    'negation': r'^(Stop|Don\'t|Never|Avoid)',
    'time_collapse': r'(\d+\s*(hours?|days?|weeks?|months?|years?))',
    'statistic': r'\d+%',
    'transformation': r'(from .+ to|went from|transformed)',
    'secret': r'(secret|hidden|nobody|never tell)',
}


def analyze_hook(hook_text: str) -> Dict:
    """
    Analyze hook effectiveness across multiple dimensions
    
    Returns:
        Dict with scores and recommendations
    """
    hook = hook_text.strip()
    
    # Score components
    scores = {
        'length': score_length(hook),
        'power_words': score_power_words(hook),
        'pattern': score_pattern(hook),
        'clarity': score_clarity(hook),
        'urgency': score_urgency(hook)
    }
    
    # Calculate overall score (0-100)
    weights = {
        'length': 0.2,
        'power_words': 0.3,
        'pattern': 0.25,
        'clarity': 0.15,
        'urgency': 0.1
    }
    
    overall = sum(scores[k] * weights[k] for k in scores)
    
    # Generate recommendations
    recommendations = generate_recommendations(hook, scores)
    
    # Detect hook type
    hook_type = detect_hook_type(hook)
    
    return {
        'hook': hook,
        'overall_score': round(overall, 1),
        'grade': get_grade(overall),
        'scores': scores,
        'hook_type': hook_type,
        'recommendations': recommendations,
        'detected_power_words': find_power_words(hook),
        'word_count': len(hook.split())
    }


def score_length(hook: str) -> float:
    """Score based on optimal hook length (5-15 words ideal)"""
    words = len(hook.split())
    
    if 5 <= words <= 15:
        return 100
    elif 3 <= words < 5 or 15 < words <= 20:
        return 70
    elif words < 3 or words > 25:
        return 30
    else:
        return 50


def score_power_words(hook: str) -> float:
    """Score based on presence of power words"""
    hook_lower = hook.lower()
    power_word_count = 0
    
    for category, words in POWER_WORDS.items():
        for word in words:
            if word in hook_lower:
                power_word_count += 1
    
    # Diminishing returns after 3 power words
    if power_word_count == 0:
        return 20
    elif power_word_count == 1:
        return 60
    elif power_word_count == 2:
        return 85
    else:
        return 100


def score_pattern(hook: str) -> float:
    """Score based on recognized viral patterns"""
    matches = 0
    
    for pattern_name, regex in HOOK_PATTERNS.items():
        if re.search(regex, hook, re.IGNORECASE):
            matches += 1
    
    # Score: 20 per pattern matched (max 100)
    return min(matches * 25, 100)


def score_clarity(hook: str) -> float:
    """Score based on clarity (no jargon, simple words)"""
    words = hook.split()
    
    # Check for overly long words (potential jargon)
    long_words = [w for w in words if len(w) > 12]
    
    # Check for common jargon indicators
    jargon_indicators = ['paradigm', 'synergy', 'leverage', 'ecosystem', 'framework']
    jargon_count = sum(1 for word in words if word.lower() in jargon_indicators)
    
    # Penalty for complexity
    penalty = (len(long_words) * 15) + (jargon_count * 20)
    
    return max(100 - penalty, 0)


def score_urgency(hook: str) -> float:
    """Score based on urgency and action orientation"""
    hook_lower = hook.lower()
    
    urgency_words = POWER_WORDS['urgency']
    urgency_count = sum(1 for word in urgency_words if word in hook_lower)
    
    # Command/imperative form (starts with verb)
    imperative_verbs = ['stop', 'start', 'learn', 'discover', 'watch', 'see', 'try']
    starts_with_verb = any(hook_lower.startswith(verb) for verb in imperative_verbs)
    
    score = 40 if starts_with_verb else 20
    score += min(urgency_count * 30, 60)
    
    return min(score, 100)


def find_power_words(hook: str) -> Dict[str, List[str]]:
    """Find all power words in the hook"""
    hook_lower = hook.lower()
    found = {}
    
    for category, words in POWER_WORDS.items():
        category_words = [w for w in words if w in hook_lower]
        if category_words:
            found[category] = category_words
    
    return found


def detect_hook_type(hook: str) -> str:
    """Detect the primary hook type"""
    hook_lower = hook.lower()
    
    # Check patterns in order of specificity
    if re.search(r'^(stop|don\'t|never)', hook_lower):
        return "Negation Hook"
    elif '?' in hook:
        return "Question Hook"
    elif re.search(r'\d+%', hook):
        return "Statistic Hook"
    elif re.search(r'(from .+ to|went from)', hook_lower):
        return "Transformation Hook"
    elif re.search(r'(secret|hidden|nobody)', hook_lower):
        return "Secret Hook"
    elif re.search(r'(\d+\s*(hours?|days?|weeks?))', hook_lower):
        return "Time Collapse Hook"
    else:
        return "Standard Hook"


def generate_recommendations(hook: str, scores: Dict[str, float]) -> List[str]:
    """Generate actionable recommendations"""
    recs = []
    words = hook.split()
    
    # Length recommendations
    if scores['length'] < 70:
        if len(words) < 5:
            recs.append("❌ Hook too short - add context (aim for 8-12 words)")
        else:
            recs.append("❌ Hook too long - trim to essential message")
    
    # Power words
    if scores['power_words'] < 60:
        recs.append("⚠️ Add power words: 'secret', 'mistake', 'nobody', 'stop', 'transform'")
    
    # Pattern
    if scores['pattern'] < 50:
        recs.append("💡 Use proven pattern: Question / Negation / Statistic / Transformation")
    
    # Clarity
    if scores['clarity'] < 70:
        recs.append("🔍 Simplify language - remove jargon or complex words")
    
    # Urgency
    if scores['urgency'] < 50:
        recs.append("⚡ Add urgency - start with action verb or use 'now', 'today'")
    
    # If score is good
    if not recs:
        recs.append("✅ Strong hook - ready to use!")
    
    return recs


def get_grade(score: float) -> str:
    """Convert numeric score to letter grade"""
    if score >= 90:
        return "A+ (Viral Potential)"
    elif score >= 80:
        return "A (Strong)"
    elif score >= 70:
        return "B (Good)"
    elif score >= 60:
        return "C (Acceptable)"
    else:
        return "D (Needs Work)"


def format_report(analysis: Dict) -> str:
    """Format analysis as readable report"""
    report = []
    report.append("=" * 60)
    report.append("🎯 HOOK ANALYSIS REPORT")
    report.append("=" * 60)
    report.append("")
    report.append(f"Hook: \"{analysis['hook']}\"")
    report.append("")
    report.append(f"📊 OVERALL SCORE: {analysis['overall_score']}/100 - {analysis['grade']}")
    report.append("")
    report.append("📈 Component Scores:")
    for component, score in analysis['scores'].items():
        bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))
        report.append(f"  {component.ljust(15)}: [{bar}] {score:.0f}/100")
    report.append("")
    report.append(f"🏷️  Hook Type: {analysis['hook_type']}")
    report.append(f"📝 Word Count: {analysis['word_count']} words")
    report.append("")
    
    if analysis['detected_power_words']:
        report.append("💪 Detected Power Words:")
        for category, words in analysis['detected_power_words'].items():
            report.append(f"  • {category.title()}: {', '.join(words)}")
        report.append("")
    
    report.append("💡 Recommendations:")
    for rec in analysis['recommendations']:
        report.append(f"  {rec}")
    report.append("")
    report.append("=" * 60)
    
    return "\n".join(report)


def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python analyze_hook.py \"Your hook text here\"")
        print("\nExample:")
        print("  python analyze_hook.py \"Stop using Docker. Here's why...\"")
        sys.exit(1)
    
    hook_text = " ".join(sys.argv[1:])
    analysis = analyze_hook(hook_text)
    print(format_report(analysis))
    
    # Return exit code based on score
    if analysis['overall_score'] >= 70:
        sys.exit(0)  # Good hook
    else:
        sys.exit(1)  # Needs improvement


if __name__ == "__main__":
    main()
