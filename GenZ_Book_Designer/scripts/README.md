# GenZ Book Designer - Helper Scripts

**Automation tools for creating viral Gen Z books with optimal engagement.**

---

## 📁 Scripts Overview

### 1. `title-scorer.py`
**Score book titles for viral potential**

Evaluates titles across 6 dimensions:
- Length optimization (40-80 chars ideal)
- Power words (urgency, rebellion, achievement)
- Emotional triggers (curiosity, FOMO, challenge)
- Numbers/specificity
- Gen Z language patterns
- Searchability

**Single title:**
```bash
python title-scorer.py "Side Hustle Speedrun: Broke to Boss in 90 Days"
```

**Batch scoring:**
```bash
python title-scorer.py --batch titles.txt
```

**Output:**
```
TITLE: Side Hustle Speedrun: Broke to Boss in 90 Days
📊 TOTAL SCORE: 87/100
🎯 GRADE: A
💬 🔥 Viral potential - Strong title!

DETAILED BREAKDOWN:
Length (51 chars)          : 20/20
Power Words                : 20/25
Emotional Triggers         : 15/20
Specificity (Numbers)      : 15/15
Gen Z Language             : 10/10
Searchability              : 7/10
```

---

### 2. `pit-stop-generator.py`
**Generate interactive engagement breaks**

Creates pit stops based on:
- Theme (marketing, finance, business, etc.)
- Type (challenge, quiz, game, reflection, checkpoint)
- Difficulty (easy, medium, hard)

**Single pit stop:**
```bash
python pit-stop-generator.py --theme marketing --type challenge
```

**Random generation:**
```bash
python pit-stop-generator.py --random
```

**Full chapter set (4 pit stops):**
```bash
python pit-stop-generator.py --chapter --theme finance
```

**Output:**
```
PIT STOP: The 5-Minute Marketing Sprint
Type: Challenge | Difficulty: Medium | Time: 5-10 min

📝 DESCRIPTION:
   Set a timer for 5-10 minutes and complete this real-world task

🎨 VISUAL DESIGN:
   Timer illustration with progress checkpoints

✅ TASKS:
   1. Open your Instagram/TikTok and find 3 examples of viral hooks
   2. Screenshot the best and worst examples
   3. Write 2-3 sentences explaining why each works or fails
   4. Tag what you learned in the margins of this page

🔓 UNLOCK REWARD:
   Marketing Framework Template
```

---

### 3. `chapter-validator.py`
**Validate manuscript structure and pacing**

Checks:
- Sub-chapter word counts (target: 800-1500 words)
- Pit stop placement (every sub-chapter)
- Hook presence (engaging chapter openings)
- Chapter naming (no boring "Chapter 1, 2, 3")
- Flow/pacing

**Validate full manuscript:**
```bash
python chapter-validator.py manuscript.txt
```

**Validate specific chapter:**
```bash
python chapter-validator.py --chapter "Chapter 1" manuscript.txt
```

**Export to JSON:**
```bash
python chapter-validator.py --json results.json manuscript.txt
```

**Output:**
```
MANUSCRIPT VALIDATION RESULTS
Chapters analyzed: 8
Status: 6/8 PASSED
Issues: 4 critical
Warnings: 7 minor

✅ Why Your Parents' Money Advice is Broke
   Total words: 4,200
   Sub-chapters: 4
   Pit stops: 4
   Avg words/sub: 1,050

❌ The $10K Side Hustle Framework
   Total words: 3,800
   Sub-chapters: 3
   Pit stops: 2
   Avg words/sub: 1,267

   ❌ CRITICAL ISSUES (2):
      • Sub-chapter 3 missing pit stop
      • Chapter name: Boring pattern detected
```

---

## 🛠️ Installation

**Requirements:**
- Python 3.7+
- No external dependencies (uses standard library only)

**Setup:**
```bash
# Navigate to scripts directory
cd GenZ_Book_Designer/scripts

# Make scripts executable (Unix/Mac)
chmod +x *.py

# Test installation
python title-scorer.py --help
```

---

## 📚 Usage Examples

### Example 1: Title Testing Workflow
```bash
# Create titles.txt with candidate titles
echo "Side Hustle Speedrun: Broke to Boss in 90 Days" > titles.txt
echo "The $10K Challenge: Make Money While You Sleep" >> titles.txt
echo "Your 9-5 is Your Side Hustle Now" >> titles.txt

# Score all titles
python title-scorer.py --batch titles.txt

# Top-scoring title is automatically ranked first
```

### Example 2: Chapter Design Workflow
```bash
# Generate complete pit stop set for a chapter
python pit-stop-generator.py --chapter --theme marketing

# Copy output into manuscript
# Then validate structure
python chapter-validator.py manuscript.txt
```

### Example 3: Manuscript Quality Check
```bash
# Before publishing, validate everything
python chapter-validator.py --json validation.json manuscript.txt

# Review critical issues
# Fix issues in manuscript
# Re-validate until all PASS
```

---

## 📖 Manuscript Format

**For chapter-validator.py to work, use this structure:**

```markdown
# Chapter Name (engaging, not "Chapter 1")

## Sub-chapter 1 Name
Content here (800-1500 words)...

### PIT STOP: Challenge Name
Pit stop content...

## Sub-chapter 2 Name
Content here (800-1500 words)...

### PIT STOP: Quiz Name
Pit stop content...
```

**Rules:**
- Use `#` for chapter headers
- Use `##` for sub-chapter headers
- Use `### PIT STOP:` for pit stops
- One pit stop per sub-chapter
- Start chapters with hooks (story, question, stat)

---

## 🎯 Best Practices

### Title Scoring
- Aim for score ≥ 70 (Grade B or higher)
- Include numbers for specificity
- Use power words naturally (not keyword stuffing)
- Keep length 40-80 characters
- Test multiple variations, pick highest score

### Pit Stop Generation
- Match pit stop type to learning objective
- Start chapters with challenges/quizzes (build momentum)
- End chapters with checkpoints (celebrate progress)
- Mix types for variety (not all challenges)
- Adjust difficulty based on chapter position

### Chapter Validation
- Target 800-1500 words per sub-chapter
- Always include pit stops (no exceptions)
- Start with strong hooks
- Avoid boring chapter names
- Re-validate after every revision

---

## 🐛 Troubleshooting

**"No chapters found" error:**
- Check markdown header syntax (# for chapters, ## for sub-chapters)
- Ensure proper spacing after # symbols
- Verify file encoding (UTF-8)

**Title scorer gives low scores:**
- Add numbers (7, 90, $10K)
- Include power words (speedrun, hack, secret)
- Make it specific (not vague)
- Use Gen Z language

**Pit stop generator seems repetitive:**
- Use --random for variety
- Manually edit templates in pit-stop-generator.py
- Add custom themes to THEME_CONFIGS

---

## 📝 Notes

- All scripts use **standard library only** (no pip install needed)
- Scripts are **standalone** (can be used without Claude)
- Output is **copy-paste ready** for manuscripts
- **Windows/Mac/Linux** compatible

---

## 🔧 Customization

To add your own themes to pit-stop-generator.py:

```python
# Edit THEME_CONFIGS dictionary
THEME_CONFIGS = {
    'yourtheme': {
        'platform': 'relevant platform',
        'concept': 'key concepts',
        'target_audience': 'ideal reader',
        'thing': 'deliverable',
        'skill': 'main skill learned',
        'achievement': 'badge name'
    }
}
```

To adjust word count targets in chapter-validator.py:

```python
# Edit these constants
WORD_COUNT_OPTIMAL = (800, 1500)  # Target range
WORD_COUNT_ACCEPTABLE = (500, 2000)  # Acceptable range
```

---

**Ready to create viral Gen Z books? Start with title-scorer.py!**
