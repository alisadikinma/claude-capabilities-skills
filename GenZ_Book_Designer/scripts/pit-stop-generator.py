#!/usr/bin/env python3
"""
Pit Stop Generator - Create engaging reader breaks for Gen Z books

Generates interactive pit stops based on:
- Chapter theme/topic
- Engagement type (challenge, game, reflection, quiz)
- Difficulty level
- Time commitment (2-5 min, 5-10 min, 10+ min)

Usage:
    python pit-stop-generator.py --theme "marketing" --type challenge
    python pit-stop-generator.py --theme "finance" --type quiz --difficulty easy
    python pit-stop-generator.py --random
"""

import sys
import random
import argparse
from typing import Dict, List

# Pit Stop Templates by Type
PIT_STOP_TEMPLATES = {
    'challenge': [
        {
            'name': 'The {time}-Minute {theme} Sprint',
            'description': 'Set a timer for {time} minutes and complete this real-world task',
            'visual': 'Timer illustration with progress checkpoints',
            'unlock': '{theme} Framework Template',
            'time': '5-10 min',
            'tasks': [
                'Open your {platform} and find 3 examples of {concept}',
                'Screenshot the best and worst examples',
                'Write 2-3 sentences explaining why each works or fails',
                'Tag what you learned in the margins of this page'
            ]
        },
        {
            'name': 'The {number}-DM Challenge',
            'description': 'Apply what you just learned by reaching out to real people',
            'visual': 'Mobile phone mockup with message bubbles',
            'unlock': 'Copy-paste message templates',
            'time': '5-10 min',
            'tasks': [
                'Find {number} {target_audience} on {platform}',
                'Send them this exact message: "{message_template}"',
                'Screenshot their responses',
                'Return here and note what worked/didn\'t work'
            ]
        },
        {
            'name': 'The "Better Than This" Challenge',
            'description': 'Prove you understood by improving bad examples',
            'visual': 'Before/After split-screen comparison',
            'unlock': '{theme} Improvement Checklist',
            'time': '5-10 min',
            'tasks': [
                'Review this intentionally bad example of {concept}',
                'List 3 mistakes you spotted',
                'Rewrite it correctly in 2-3 sentences',
                'Compare your version to the solution on the next page'
            ]
        }
    ],
    
    'quiz': [
        {
            'name': '{theme} Reality Check',
            'description': 'Quick multiple choice to test your understanding',
            'visual': 'Colorful answer bubbles (A/B/C/D)',
            'unlock': 'Score-based bonus content',
            'time': '2-5 min',
            'format': 'Multiple choice (5 questions)',
            'questions': [
                'Based on what you just read, which approach works best for {scenario}?',
                'What\'s the biggest mistake beginners make with {concept}?',
                'If you only had {constraint}, which strategy should you use?',
                'Which of these is a red flag for {problem}?',
                'What should you do first when {situation}?'
            ]
        },
        {
            'name': 'Spot the {theme} Fail',
            'description': 'Identify what\'s wrong in these real examples',
            'visual': 'Example screenshots with clickable hotspots',
            'unlock': 'Fail analysis breakdown',
            'time': '5 min',
            'format': 'Visual identification (3-4 examples)',
            'tasks': [
                'Look at Example A: What\'s the main problem?',
                'Example B vs Example C: Which follows the rules you learned?',
                'Example D: How would you fix this?'
            ]
        }
    ],
    
    'game': [
        {
            'name': '{theme} Swipe Game',
            'description': 'Swipe left (bad) or right (good) on real examples',
            'visual': 'Tinder-style card interface',
            'unlock': 'Pattern recognition guide',
            'time': '3-5 min',
            'mechanics': 'Show 10 examples, reader swipes left/right, instant feedback'
        },
        {
            'name': 'Build Your {thing}',
            'description': 'Assemble components to create a working {thing}',
            'visual': 'Drag-and-drop interface with puzzle pieces',
            'unlock': 'Your custom {thing} saved as template',
            'time': '5-10 min',
            'mechanics': 'Reader drags components (headline, hook, CTA, etc.) to build complete example'
        },
        {
            'name': 'The {theme} Simulator',
            'description': 'Make decisions and see immediate results',
            'visual': 'Choose-your-own-adventure flowchart',
            'unlock': 'Decision tree for real scenarios',
            'time': '5-10 min',
            'mechanics': 'Reader makes 3-4 strategic choices, sees consequences, learns optimal path'
        }
    ],
    
    'reflection': [
        {
            'name': 'Your {theme} Audit',
            'description': 'Honest self-assessment before moving forward',
            'visual': 'Checkbox grid with progress bars',
            'unlock': 'Personalized next steps',
            'time': '5 min',
            'prompts': [
                'On a scale of 1-10, how confident are you with {concept}?',
                'Which of these 3 mistakes have you made?',
                'What\'s your biggest {theme} challenge right now?',
                'Before reading this chapter, what would you have done differently?'
            ]
        },
        {
            'name': 'The "{theme}" Mindset Check',
            'description': 'Identify limiting beliefs holding you back',
            'visual': 'Two-column comparison (Old Mindset vs New Mindset)',
            'unlock': 'Mindset shift affirmations',
            'time': '3-5 min',
            'format': 'Match old beliefs to new perspectives',
            'prompts': [
                'What did you believe about {theme} before this chapter?',
                'What\'s the new perspective you\'re adopting?',
                'What would change if you fully believed this?'
            ]
        }
    ],
    
    'checkpoint': [
        {
            'name': '🎯 You\'ve Unlocked: {achievement}',
            'description': 'Progress milestone with gamification',
            'visual': 'Achievement badge + progress bar',
            'unlock': 'Bonus {theme} resource',
            'time': '1 min',
            'elements': [
                'Progress bar showing % of book completed',
                'Achievement badge (collect all {number})',
                'Quick recap: "You now know how to {skill}"',
                'Teaser for next section'
            ]
        }
    ]
}

# Theme-specific customization
THEME_CONFIGS = {
    'marketing': {
        'platform': 'Instagram/TikTok/LinkedIn',
        'concept': 'viral hooks/engagement tactics/CTAs',
        'target_audience': 'brands in your niche',
        'thing': 'ad campaign/landing page/content calendar',
        'skill': 'craft scroll-stopping hooks',
        'achievement': 'Marketing Foundations'
    },
    'finance': {
        'platform': 'bank app/investment dashboard',
        'concept': 'budgeting/compound interest/risk assessment',
        'target_audience': 'financially successful people',
        'thing': 'budget plan/investment strategy',
        'skill': 'manage money like a pro',
        'achievement': 'Financial Literacy'
    },
    'business': {
        'platform': 'LinkedIn/Twitter',
        'concept': 'value propositions/business models/pricing',
        'target_audience': 'potential customers/partners',
        'thing': 'business plan/pitch deck',
        'skill': 'validate business ideas',
        'achievement': 'Entrepreneur Mindset'
    },
    'productivity': {
        'platform': 'calendar app/Notion',
        'concept': 'time blocking/deep work/prioritization',
        'target_audience': 'high performers',
        'thing': 'productivity system/daily routine',
        'skill': 'maximize your output',
        'achievement': 'Peak Performance'
    },
    'content': {
        'platform': 'TikTok/YouTube/Instagram',
        'concept': 'storytelling/editing/thumbnails',
        'target_audience': 'creators in your niche',
        'thing': 'content plan/video script',
        'skill': 'create viral content',
        'achievement': 'Content Creator'
    }
}

def generate_pit_stop(theme: str, pit_type: str, difficulty: str = 'medium') -> Dict:
    """
    Generate a complete pit stop based on parameters
    
    Args:
        theme: Topic/domain (marketing, finance, business, etc.)
        pit_type: Type of engagement (challenge, quiz, game, reflection, checkpoint)
        difficulty: easy/medium/hard (affects time and complexity)
    
    Returns:
        Dict with complete pit stop specification
    """
    # Get theme config (use generic if theme not found)
    theme_config = THEME_CONFIGS.get(theme.lower(), {
        'platform': 'relevant platform',
        'concept': 'core concepts',
        'target_audience': 'relevant people',
        'thing': 'project',
        'skill': 'apply these principles',
        'achievement': f'{theme.title()} Mastery'
    })
    
    # Select random template from type
    templates = PIT_STOP_TEMPLATES.get(pit_type, PIT_STOP_TEMPLATES['challenge'])
    template = random.choice(templates)
    
    # Customize based on difficulty
    time_ranges = {
        'easy': '2-5 min',
        'medium': '5-10 min',
        'hard': '10-15 min'
    }
    
    # Fill template placeholders
    pit_stop = {}
    for key, value in template.items():
        if isinstance(value, str):
            pit_stop[key] = value.format(
                theme=theme.lower(),
                time=time_ranges.get(difficulty, '5-10'),
                number=random.choice(['3', '5', '7', '10']),
                **theme_config
            )
        else:
            pit_stop[key] = value
    
    # Add metadata
    pit_stop['theme'] = theme
    pit_stop['type'] = pit_type
    pit_stop['difficulty'] = difficulty
    
    return pit_stop


def print_pit_stop(pit_stop: Dict):
    """Pretty print pit stop specification"""
    print("\n" + "="*70)
    print(f"PIT STOP: {pit_stop['name']}")
    print("="*70)
    print(f"\nType: {pit_stop['type'].title()} | Difficulty: {pit_stop['difficulty'].title()} | Time: {pit_stop.get('time', 'N/A')}")
    print(f"\n📝 DESCRIPTION:")
    print(f"   {pit_stop['description']}")
    
    print(f"\n🎨 VISUAL DESIGN:")
    print(f"   {pit_stop['visual']}")
    
    if 'tasks' in pit_stop:
        print(f"\n✅ TASKS:")
        for i, task in enumerate(pit_stop['tasks'], 1):
            print(f"   {i}. {task}")
    
    if 'questions' in pit_stop:
        print(f"\n❓ QUESTIONS:")
        for i, q in enumerate(pit_stop['questions'], 1):
            print(f"   {i}. {q}")
    
    if 'prompts' in pit_stop:
        print(f"\n💭 REFLECTION PROMPTS:")
        for i, p in enumerate(pit_stop['prompts'], 1):
            print(f"   {i}. {p}")
    
    if 'mechanics' in pit_stop:
        print(f"\n🎮 GAME MECHANICS:")
        print(f"   {pit_stop['mechanics']}")
    
    if 'elements' in pit_stop:
        print(f"\n🏆 CHECKPOINT ELEMENTS:")
        for elem in pit_stop['elements']:
            print(f"   • {elem}")
    
    print(f"\n🔓 UNLOCK REWARD:")
    print(f"   {pit_stop['unlock']}")
    
    print("\n" + "="*70 + "\n")


def generate_chapter_set(theme: str, num_substops: int = 4) -> List[Dict]:
    """Generate a full set of pit stops for a chapter"""
    types = ['challenge', 'quiz', 'game', 'reflection', 'checkpoint']
    
    # Ensure variety
    selected_types = []
    for i in range(num_substops):
        if i == 0:
            # First pit stop: usually challenge or quiz
            selected_types.append(random.choice(['challenge', 'quiz']))
        elif i == num_substops - 1:
            # Last pit stop: checkpoint
            selected_types.append('checkpoint')
        else:
            # Middle pit stops: mix it up
            selected_types.append(random.choice(['challenge', 'quiz', 'game', 'reflection']))
    
    pit_stops = []
    for i, pit_type in enumerate(selected_types, 1):
        difficulty = 'easy' if i == 1 else 'medium'
        pit_stop = generate_pit_stop(theme, pit_type, difficulty)
        pit_stop['sub_chapter'] = i
        pit_stops.append(pit_stop)
    
    return pit_stops


def main():
    parser = argparse.ArgumentParser(description='Generate Gen Z pit stops for book chapters')
    parser.add_argument('--theme', type=str, help='Chapter theme (marketing, finance, business, etc.)')
    parser.add_argument('--type', type=str, choices=['challenge', 'quiz', 'game', 'reflection', 'checkpoint'], help='Pit stop type')
    parser.add_argument('--difficulty', type=str, choices=['easy', 'medium', 'hard'], default='medium', help='Difficulty level')
    parser.add_argument('--random', action='store_true', help='Generate random pit stop')
    parser.add_argument('--chapter', action='store_true', help='Generate full chapter set (4 pit stops)')
    
    args = parser.parse_args()
    
    if args.chapter:
        if not args.theme:
            print("❌ Error: --theme required for chapter mode")
            print("Example: python pit-stop-generator.py --chapter --theme marketing")
            sys.exit(1)
        
        print(f"\n📚 Generating complete chapter pit stop set for: {args.theme.upper()}")
        print("="*70)
        
        pit_stops = generate_chapter_set(args.theme)
        for pit_stop in pit_stops:
            print(f"\n[SUB-CHAPTER {pit_stop['sub_chapter']}]")
            print_pit_stop(pit_stop)
    
    elif args.random:
        theme = random.choice(list(THEME_CONFIGS.keys()))
        pit_type = random.choice(list(PIT_STOP_TEMPLATES.keys()))
        difficulty = random.choice(['easy', 'medium', 'hard'])
        
        print(f"\n🎲 Random pit stop generated!")
        pit_stop = generate_pit_stop(theme, pit_type, difficulty)
        print_pit_stop(pit_stop)
    
    else:
        if not args.theme or not args.type:
            print(__doc__)
            print("\nExamples:")
            print("  python pit-stop-generator.py --theme marketing --type challenge")
            print("  python pit-stop-generator.py --theme finance --type quiz --difficulty easy")
            print("  python pit-stop-generator.py --chapter --theme business")
            print("  python pit-stop-generator.py --random")
            sys.exit(1)
        
        pit_stop = generate_pit_stop(args.theme, args.type, args.difficulty)
        print_pit_stop(pit_stop)


if __name__ == '__main__':
    main()
