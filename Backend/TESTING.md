# Model Testing Guide

This directory contains comprehensive test scripts for testing the LughaBridge translation models (ASR, Translation, and TTS).

## Prerequisites

Ensure you have:
1. Downloaded all required models using `python manage.py download_models`
2. Activated your virtual environment
3. All dependencies installed from `requirements.txt`

## Test Scripts

### 1. Quick Model Loading Test
**File:** `test_model_loading.py`

Tests that all models can be loaded successfully without errors.

```bash
cd Backend
python test_model_loading.py
```

**What it tests:**
- Loads all ASR models (Kikuyu, Swahili, English)
- Loads the NLLB translation model
- Loads all TTS models (Kikuyu, Swahili, English)
- Reports success/failure for each model

**Output:** Simple pass/fail status for each model with summary

---

### 2. Translation Functionality Test
**File:** `test_translation_samples.py`

Tests the translation service with real text examples in multiple languages.

```bash
cd Backend
python test_translation_samples.py
```

**What it tests:**
- English ↔ Swahili translations
- English ↔ Kikuyu translations
- Swahili ↔ Kikuyu translations
- Round-trip translations (A → B → A)
- Various text categories: greetings, questions, common phrases, longer texts

**Output:** Translation results with confidence scores for each test case

---

### 3. TTS Sample Generation
**File:** `test_tts_samples.py`

Tests Text-to-Speech and generates sample audio files for all supported languages.

```bash
cd Backend
python test_tts_samples.py
```

**What it tests:**
- TTS synthesis for English, Swahili, and Kikuyu
- Different text lengths (short, medium, long)
- Numbers, questions, and various phrases
- Audio file properties (duration, sample rate, file size)

**Output:** 
- Audio samples saved to `media/tts_samples/`
- Detailed information about each generated audio file

---

### 4. Comprehensive Model Test
**File:** `test_models_comprehensive.py`

Complete end-to-end testing of all services including a full translation pipeline.

```bash
cd Backend
python test_models_comprehensive.py
```

**What it tests:**
- **ASR Service:** Model loading, audio transcription (with generated test audio)
- **Translation Service:** Text translation in all language pairs
- **TTS Service:** Speech synthesis with sample texts
- **Full Pipeline:** Text → TTS → ASR → Translation → TTS

**Output:** Detailed logs of each step with results and confidence scores

---

## Understanding the Models

### ASR (Automatic Speech Recognition)
Converts speech audio to text.

**Models:**
- Kikuyu: `badrex/w2v-bert-2.0-kikuyu-asr`
- Swahili: `thinkKenya/wav2vec2-large-xls-r-300m-sw`
- English: `facebook/wav2vec2-large-960h-lv60-self`

**Expected input:** Audio file (WAV, MP3, etc.) at 16kHz sample rate
**Output:** `{"text": str, "confidence": float}`

### Translation
Translates text between languages using NLLB (No Language Left Behind).

**Model:** `facebook/nllb-200-distilled-600M`

**Language codes:**
- Kikuyu: `kik_Latn`
- Swahili: `swh_Latn`
- English: `eng_Latn`

**Expected input:** Text string
**Output:** `{"text": str, "confidence": float}`

### TTS (Text-to-Speech)
Converts text to speech audio using MMS-TTS.

**Models:**
- Kikuyu: `facebook/mms-tts-kik`
- Swahili: `facebook/mms-tts-swh`
- English: `facebook/mms-tts-eng`

**Expected input:** Text string
**Output:** Path to generated WAV file (16kHz)

---

## Running Tests

### Run All Tests
```bash
# Quick verification
python test_model_loading.py

# Test translation
python test_translation_samples.py

# Test TTS and generate samples
python test_tts_samples.py

# Comprehensive testing
python test_models_comprehensive.py
```

### Expected Results

1. **Model Loading:** All 7 models should load successfully
2. **Translation:** Translations should be coherent and contextually appropriate
3. **TTS:** Audio files should be generated in `media/tts_samples/` and `media/tts_temp/`
4. **ASR:** Transcriptions should work (note: synthetic test audio may produce gibberish)

### Troubleshooting

**Models not found:**
```bash
python manage.py download_models
```

**CUDA/GPU errors:**
- Tests work on both CPU and GPU
- GPU is used automatically if available
- CPU will be slower but functional

**Import errors:**
```bash
pip install -r requirements.txt
```

**Permission errors:**
- Ensure `media/` directory is writable
- Check that you're running from the Backend directory

---

## Sample Test Outputs

### Model Loading Test
```
Testing ASR Models:
  [KIKUYU] Loading badrex/w2v-bert-2.0-kikuyu-asr...
  ✓ KIKUYU ASR model loaded successfully

  [SWAHILI] Loading thinkKenya/wav2vec2-large-xls-r-300m-sw...
  ✓ SWAHILI ASR model loaded successfully

Testing Translation Model:
  ✓ NLLB translation model loaded successfully

Testing TTS Models:
  ✓ KIKUYU TTS model loaded successfully
  ✓ SWAHILI TTS model loaded successfully
  ✓ ENGLISH TTS model loaded successfully

Test Summary:
  Total:  7
  Passed: 7 ✓
  Failed: 0 ✗
  Success Rate: 100.0%
```

### Translation Test
```
Test #1:
  Direction: English → Swahili
  Source:    Hello, how are you today?
  Target:    Habari, unafanya nini leo?
  Confidence: 0.876
```

### TTS Test
```
Sample 1:
  Text: "Hello, welcome to LughaBridge."
  ✓ Generated: english_1.wav
    - Duration: 2.34 seconds
    - Sample rate: 16000 Hz
    - File size: 75,082 bytes
```

---

## Testing with Real Audio

For ASR testing with real audio files:

```python
from translation.services.huggingface_asr import HuggingFaceASR

asr = HuggingFaceASR()
result = asr.transcribe('/path/to/audio.wav', 'english')
print(f"Transcription: {result['text']}")
print(f"Confidence: {result['confidence']}")
```

## Next Steps

After verifying models work:
1. Test with real audio recordings
2. Integrate with Django views
3. Test WebSocket consumers
4. Test full room-based translation flow

---

## Notes

- First run of each test will be slower as models are loaded
- Models are cached in `HF_CACHE_DIR` after first download
- GPU significantly speeds up inference (especially for TTS and Translation)
- ASR tests with synthetic audio won't produce meaningful transcriptions
- TTS output quality depends on text complexity and language support

