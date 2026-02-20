"""
Test TTS (Text-to-Speech) functionality and generate sample audio files.

Usage:
    python test_tts_samples.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lughabridge.settings')
django.setup()

import scipy.io.wavfile as wavfile
from translation.services.mms_tts import MMSTTS


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def get_audio_info(audio_path):
    """Get information about an audio file."""
    if not os.path.exists(audio_path):
        return None
    
    sample_rate, audio_data = wavfile.read(audio_path)
    duration = len(audio_data) / sample_rate
    file_size = os.path.getsize(audio_path)
    
    return {
        'sample_rate': sample_rate,
        'duration': duration,
        'file_size': file_size,
        'samples': len(audio_data),
    }


def test_tts_synthesis():
    """Test TTS synthesis with sample texts."""
    print_header("TTS (Text-to-Speech) Sample Generation")
    
    # Initialize TTS service
    print("Initializing MMS-TTS service...")
    tts = MMSTTS()
    print(f"✓ TTS service initialized\n")
    
    # Sample texts for each language
    test_samples = [
        # English samples
        {
            'language': 'english',
            'samples': [
                'Hello, welcome to LughaBridge.',
                'This is a test of the text to speech system.',
                'How are you doing today?',
                'Thank you for using our translation service.',
                'One, two, three, four, five.',
            ]
        },
        # Swahili samples
        {
            'language': 'swahili',
            'samples': [
                'Habari, karibu LughaBridge.',
                'Hii ni jaribio la mfumo wa kusoma maandishi.',
                'Unafanya nini leo?',
                'Asante kwa kutumia huduma yetu ya tafsiri.',
                'Moja, mbili, tatu, nne, tano.',
            ]
        },
        # Kikuyu samples
        {
            'language': 'kikuyu',
            'samples': [
                'Wĩ mwega.',
                'Ũrĩa ũrĩ?',
                'Nĩ wega mũno.',
            ]
        },
    ]
    
    # Create output directory for samples
    samples_dir = os.path.join(os.path.dirname(__file__), 'media', 'tts_samples')
    os.makedirs(samples_dir, exist_ok=True)
    
    total_generated = 0
    
    for lang_group in test_samples:
        lang = lang_group['language']
        samples = lang_group['samples']
        
        print(f"\n{'─' * 80}")
        print(f"  {lang.upper()} Samples")
        print(f"{'─' * 80}\n")
        
        # Load model for this language
        try:
            print(f"Loading {lang} TTS model...")
            tts._load_model(lang)
            print(f"✓ Model loaded: {tts.model_configs[lang]}\n")
            
        except Exception as e:
            print(f"✗ Error loading model: {str(e)}\n")
            continue
        
        # Generate speech for each sample
        for i, text in enumerate(samples, 1):
            try:
                print(f"Sample {i}:")
                print(f"  Text: \"{text}\"")
                
                # Synthesize speech
                audio_path = tts.synthesize(text, lang)
                
                # Copy to samples directory with descriptive name
                sample_filename = f"{lang}_{i}.wav"
                sample_path = os.path.join(samples_dir, sample_filename)
                
                # Read and rewrite to new location
                sample_rate, audio_data = wavfile.read(audio_path)
                wavfile.write(sample_path, sample_rate, audio_data)
                
                # Get audio info
                info = get_audio_info(sample_path)
                
                if info:
                    print(f"  ✓ Generated: {sample_filename}")
                    print(f"    - Duration: {info['duration']:.2f} seconds")
                    print(f"    - Sample rate: {info['sample_rate']} Hz")
                    print(f"    - File size: {info['file_size']:,} bytes")
                    print(f"    - Path: {sample_path}")
                    total_generated += 1
                else:
                    print(f"  ✗ Error: Could not read generated audio")
                
                print()
                
            except Exception as e:
                print(f"  ✗ Error: {str(e)}\n")
    
    # Print summary
    print("=" * 80)
    print(f"  Summary: Generated {total_generated} audio samples")
    print(f"  Location: {samples_dir}")
    print("=" * 80 + "\n")


def test_tts_variations():
    """Test TTS with different text variations."""
    print_header("TTS Text Variation Tests")
    
    tts = MMSTTS()
    
    test_cases = [
        {
            'language': 'english',
            'description': 'Short greeting',
            'text': 'Hello!',
        },
        {
            'language': 'english',
            'description': 'Medium sentence',
            'text': 'The quick brown fox jumps over the lazy dog.',
        },
        {
            'language': 'english',
            'description': 'Long sentence',
            'text': 'LughaBridge is a real-time multilingual translation platform that enables seamless communication between speakers of Kikuyu, Swahili, and English.',
        },
        {
            'language': 'swahili',
            'description': 'Numbers',
            'text': 'Moja, mbili, tatu, nne, tano, sita, saba, nane, tisa, kumi.',
        },
        {
            'language': 'swahili',
            'description': 'Question',
            'text': 'Habari gani? Unafanya nini?',
        },
    ]
    
    for i, test in enumerate(test_cases, 1):
        lang = test['language']
        
        print(f"Test #{i}: {test['description']}")
        print(f"  Language: {lang.capitalize()}")
        print(f"  Text: \"{test['text']}\"")
        print(f"  Length: {len(test['text'])} characters")
        
        try:
            # Load model if needed
            if lang not in tts.models:
                tts._load_model(lang)
            
            # Synthesize
            audio_path = tts.synthesize(test['text'], lang)
            info = get_audio_info(audio_path)
            
            if info:
                print(f"  ✓ Generated successfully")
                print(f"    - Duration: {info['duration']:.2f}s")
                print(f"    - File size: {info['file_size']:,} bytes")
            else:
                print(f"  ✗ Error reading audio file")
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
        
        print()
    
    print("=" * 80 + "\n")


def main():
    """Run all TTS tests."""
    try:
        test_tts_synthesis()
        test_tts_variations()
        
        print("✓ All TTS tests completed successfully!\n")
        
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.\n")
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
