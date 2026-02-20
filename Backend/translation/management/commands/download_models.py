"""
Django management command to pre-download all translation models.
Usage: python manage.py download_models
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from translation.services.huggingface_asr import HuggingFaceASR
from translation.services.nllb_translator import NLLBTranslator
from translation.services.mms_tts import MMSTTS


class Command(BaseCommand):
    help = 'Pre-download all Hugging Face models for translation pipeline'

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            type=str,
            default=None,
            help='Download models for specific language only (kikuyu, swahili, english)',
        )

    def handle(self, *args, **options):
        language = options.get('language')
        
        if settings.DEMO_MODE:
            self.stdout.write(self.style.WARNING(
                'DEMO_MODE is enabled. Models will not be downloaded. '
                'Set DEMO_MODE=false in .env to download real models.'
            ))
            return
        
        if settings.USE_HF_INFERENCE:
            self.stdout.write(self.style.WARNING(
                'USE_HF_INFERENCE is enabled. Models are hosted on Hugging Face cloud. '
                'No local model downloads needed. '
                'Set USE_HF_INFERENCE=false in .env to download models locally.'
            ))
            return
        
        self.stdout.write(self.style.SUCCESS('Starting model downloads...'))
        self.stdout.write(f'Cache directory: {settings.HF_CACHE_DIR}')
        
        if settings.HF_TOKEN:
            self.stdout.write(self.style.SUCCESS('✓ Using authenticated HF token'))
        else:
            self.stdout.write(self.style.WARNING(
                '⚠ No HF_TOKEN set. Downloads may be slower. '
                'Get a token from https://huggingface.co/settings/tokens'
            ))
        
        self.stdout.write('')
        
        try:
            # Download ASR models
            if language:
                self._download_asr(language)
            else:
                for lang in settings.SUPPORTED_LANGUAGES:
                    if lang in settings.MODELS['asr']:
                        self._download_asr(lang)
            
            # Download translation model (shared across languages)
            self._download_translator()
            
            # Download TTS models
            if language:
                self._download_tts(language)
            else:
                for lang in settings.SUPPORTED_LANGUAGES:
                    if lang in settings.MODELS['tts']:
                        self._download_tts(lang)
            
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('✓ All models downloaded successfully!'))
            self.stdout.write(self.style.SUCCESS('You can now use DEMO_MODE=false in production.'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error downloading models: {str(e)}'))
            raise

    def _download_asr(self, language):
        """Download ASR model for specified language."""
        model_name = settings.MODELS['asr'].get(language)
        if not model_name:
            self.stdout.write(self.style.WARNING(f'⚠ No ASR model configured for {language}'))
            return
        
        self.stdout.write(f'Downloading ASR model for {language}: {model_name}')
        asr = HuggingFaceASR()
        asr._load_model(language)
        self.stdout.write(self.style.SUCCESS(f'  ✓ ASR model loaded for {language}'))

    def _download_translator(self):
        """Download translation model."""
        model_name = settings.MODELS['translation']['model']
        self.stdout.write(f'Downloading translation model: {model_name}')
        translator = NLLBTranslator()
        translator._load_model()
        self.stdout.write(self.style.SUCCESS('  ✓ Translation model loaded'))

    def _download_tts(self, language):
        """Download TTS model for specified language."""
        model_name = settings.MODELS['tts'].get(language)
        if not model_name:
            self.stdout.write(self.style.WARNING(f'⚠ No TTS model configured for {language}'))
            return
        
        self.stdout.write(f'Downloading TTS model for {language}: {model_name}')
        tts = MMSTTS()
        tts._load_model(language)
        self.stdout.write(self.style.SUCCESS(f'  ✓ TTS model loaded for {language}'))
