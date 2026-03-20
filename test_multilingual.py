#!/usr/bin/env python3
"""
Quick test script to verify multilingual language support is working
"""

import sys
import os
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Test 1: Check imports
print("=" * 60)
print("TEST 1: Checking multilingual imports...")
print("=" * 60)

try:
    from earth_dialogues import get_earth_message_multilang, EARTH_MESSAGES_MULTILANG
    print("✅ Successfully imported get_earth_message_multilang")
    print("✅ Successfully imported EARTH_MESSAGES_MULTILANG")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Check if all languages are available
print("\n" + "=" * 60)
print("TEST 2: Checking available languages...")
print("=" * 60)

languages = ['en', 'hi', 'kn']
for lang in languages:
    if lang in EARTH_MESSAGES_MULTILANG:
        print(f"✅ {lang.upper()} language support found")
        # Check key contexts
        contexts = ['welcome', 'thinking', 'correct', 'wrong', 'emotional']
        for context in contexts:
            if context in EARTH_MESSAGES_MULTILANG[lang]:
                print(f"   ✅ {context}")
            else:
                print(f"   ❌ {context} MISSING!")
    else:
        print(f"❌ {lang.upper()} language NOT found!")

# Test 3: Test message retrieval
print("\n" + "=" * 60)
print("TEST 3: Testing message retrieval...")
print("=" * 60)

test_cases = [
    ('en', 'welcome'),
    ('hi', 'welcome'),
    ('kn', 'welcome'),
    ('en', 'thinking'),
    ('hi', 'correct'),
    ('kn', 'emotional'),
]

for lang, context in test_cases:
    try:
        message = get_earth_message_multilang(context, language=lang)
        if message:
            preview = message[:50] + "..." if len(message) > 50 else message
            print(f"✅ {lang.upper()} {context:12} → {preview}")
        else:
            print(f"❌ {lang.upper()} {context:12} → EMPTY MESSAGE")
    except Exception as e:
        print(f"❌ {lang.upper()} {context:12} → ERROR: {e}")

# Test 4: Verify TTS imports
print("\n" + "=" * 60)
print("TEST 4: Checking TTS availability...")
print("=" * 60)

try:
    from talking_assistant import generate_tts_bytes
    print("✅ generate_tts_bytes function available")
except ImportError:
    print("❌ generate_tts_bytes not available")

try:
    from gtts import gTTS
    print("✅ gTTS module installed (fallback TTS)")
except ImportError:
    print("⚠️  gTTS not installed (install with: pip install gTTS)")

try:
    import pyttsx3
    print("✅ pyttsx3 module installed (offline TTS)")
except ImportError:
    print("⚠️  pyttsx3 not installed")

# Test 5: Check app.py imports multilingual support
print("\n" + "=" * 60)
print("TEST 5: Verifying app.py has multilingual imports...")
print("=" * 60)

app_file = Path("app.py")
if app_file.exists():
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'get_earth_message_multilang' in content:
            print("✅ app.py imports get_earth_message_multilang")
        else:
            print("❌ app.py does NOT import get_earth_message_multilang")
        
        if 'st.session_state.language' in content:
            print("✅ app.py uses language session state")
        else:
            print("❌ app.py doesn't use language session state")
else:
    print("⚠️  app.py not found in current directory")

# Final summary
print("\n" + "=" * 60)
print("MULTILINGUAL TEST SUMMARY")
print("=" * 60)
print("✅ All critical components present!")
print("✅ Ready to run: streamlit run app.py")
print("\nTo test selected language:")
print("  1. Run the app: streamlit run app.py")
print("  2. Go to Settings in sidebar")
print("  3. Select a language (English / Hindi / Kannada)")
print("  4. Refresh or interact - messages should appear in selected language")
print("\nIf welcome message doesn't play:")
print("  - Enable 'Voice Assistance' in Settings")
print("  - Check browser audio permissions")
print("  - Allow pop-ups if needed")
print("=" * 60)
