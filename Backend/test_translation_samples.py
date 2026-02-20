"""
Test translation functionality with sample text inputs.

Usage:
    python test_translation_samples.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lughabridge.settings')
django.setup()

from translation.services.nllb_translator import NLLBTranslator


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def test_translations():
    """Test translation with various sample sentences."""
    print_header("LughaBridge Translation Tests")
    
    # Initialize translator
    print("Initializing NLLB translator...")
    translator = NLLBTranslator()
    translator._load_model()
    print("✓ Model loaded\n")
    
    # Test cases with various language pairs
    test_cases = [
        # English to Swahili
        {
            'category': 'Greetings',
            'text': 'Hello, how are you today?',
            'source': 'english',
            'target': 'swahili',
        },
        {
            'category': 'Greetings',
            'text': 'Good morning, my friend.',
            'source': 'english',
            'target': 'swahili',
        },
        {
            'category': 'Common Phrases',
            'text': 'Thank you very much for your help.',
            'source': 'english',
            'target': 'swahili',
        },
        {
            'category': 'Questions',
            'text': 'What is your name?',
            'source': 'english',
            'target': 'swahili',
        },
        
        # Swahili to English
        {
            'category': 'Greetings',
            'text': 'Habari za asubuhi?',
            'source': 'swahili',
            'target': 'english',
        },
        {
            'category': 'Greetings',
            'text': 'Jambo! Karibu Tanzania.',
            'source': 'swahili',
            'target': 'english',
        },
        {
            'category': 'Common Phrases',
            'text': 'Asante sana kwa msaada wako.',
            'source': 'swahili',
            'target': 'english',
        },
        {
            'category': 'Questions',
            'text': 'Jina lako ni nani?',
            'source': 'swahili',
            'target': 'english',
        },
        
        # English to Kikuyu
        {
            'category': 'Greetings',
            'text': 'Hello, how are you?',
            'source': 'english',
            'target': 'kikuyu',
        },
        {
            'category': 'Common Phrases',
            'text': 'Thank you for coming.',
            'source': 'english',
            'target': 'kikuyu',
        },
        
        # Kikuyu to English
        {
            'category': 'Greetings',
            'text': 'Wĩ mwega',
            'source': 'kikuyu',
            'target': 'english',
        },
        
        # Swahili to Kikuyu
        {
            'category': 'Greetings',
            'text': 'Habari yako?',
            'source': 'swahili',
            'target': 'kikuyu',
        },
        
        # Longer text
        {
            'category': 'Longer Text',
            'text': 'Welcome to our conference. Today we will discuss important topics about technology and innovation in East Africa.',
            'source': 'english',
            'target': 'swahili',
        },
    ]
    
    # Group by category
    current_category = None
    
    for i, test in enumerate(test_cases, 1):
        # Print category header if new category
        if test['category'] != current_category:
            print(f"\n{'─' * 80}")
            print(f"  {test['category']}")
            print(f"{'─' * 80}\n")
            current_category = test['category']
        
        # Perform translation
        try:
            print(f"Test #{i}:")
            print(f"  Direction: {test['source'].capitalize()} → {test['target'].capitalize()}")
            print(f"  Source:    {test['text']}")
            
            result = translator.translate(
                test['text'],
                test['source'],
                test['target']
            )
            
            print(f"  Target:    {result['text']}")
            print(f"  Confidence: {result['confidence']:.3f}")
            print()
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}\n")
    
    print("=" * 80)
    print("  Translation tests completed")
    print("=" * 80 + "\n")


def test_bidirectional_translation():
    """Test round-trip translation (A -> B -> A)."""
    print_header("Round-Trip Translation Test")
    
    translator = NLLBTranslator()
    translator._load_model()
    
    test_cases = [
        {
            'text': 'Hello, how are you?',
            'lang1': 'english',
            'lang2': 'swahili',
        },
        {
            'text': 'Thank you for your help.',
            'lang1': 'english',
            'lang2': 'swahili',
        },
        {
            'text': 'Habari za leo?',
            'lang1': 'swahili',
            'lang2': 'english',
        },
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test #{i}:")
        print(f"  Original ({test['lang1']}): {test['text']}")
        
        try:
            # First translation
            result1 = translator.translate(
                test['text'],
                test['lang1'],
                test['lang2']
            )
            print(f"  Translated ({test['lang2']}): {result1['text']}")
            print(f"  Confidence: {result1['confidence']:.3f}")
            
            # Back translation
            result2 = translator.translate(
                result1['text'],
                test['lang2'],
                test['lang1']
            )
            print(f"  Back-translated ({test['lang1']}): {result2['text']}")
            print(f"  Confidence: {result2['confidence']:.3f}")
            print()
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}\n")
    
    print("=" * 80 + "\n")


def main():
    """Run all translation tests."""
    try:
        test_translations()
        test_bidirectional_translation()
        
        print("✓ All translation tests completed successfully!\n")
        
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.\n")
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
