from deep_translator import GoogleTranslator, DeepL, YandexTranslator
from deep_translator.exceptions import InvalidSourceOrTargetLanguage, LanguageNotSupportedException
from loguru import logger


class TranslatorManager:

    supported_apis = [
        "GoogleTranslator",
        "YandexTranslator",
        "DeepLTranslator"
    ]

    def __init__(
            self,
            source_language='english',
            target_language='russian',
            api_service=None,
            api_key=None,
    ):
        self._source_language = source_language
        self._target_language = target_language
        self._api_service = api_service
        self._api_key = api_key

        self._init_translator_obj()

    @logger.catch()
    def _init_translator_obj(self):
        try:
            match self._api_service:
                case 'GoogleTranslator':
                    self._translator = GoogleTranslator(source=self._source_language,
                                                        target=self._target_language)
                case 'DeepLTranslator':
                    self._translator = DeepL(api_key=self._api_key,
                                             source=self._source_language,
                                             target=self._target_language)
                case 'YandexTranslator':
                    self._translator = YandexTranslator(api_key=self._api_key,
                                                        source=self._source_language,
                                                        target=self._target_language)
                case _:
                    self._translator = None
        except InvalidSourceOrTargetLanguage:
            logger.warning(f'Source {self._source_language} and target {self._target_language} languages is same')
        except LanguageNotSupportedException:
            logger.warning(f'Source {self._source_language} and target {self._target_language} not supported in {self._api_service}')

    def set_new_api_service(self, api_service, api_key=None):
        self._api_service = api_service
        self._api_key = api_key
        self._init_translator_obj()

    def set_new_source_language(self, new_source: str):
        self._source_language = new_source
        self._init_translator_obj()

    def set_new_target_language(self, new_target: str):
        self._target_language = new_target
        self._init_translator_obj()

    def get_supported_languages(self):
        return self._translator.get_supported_languages()

    def translate(self, text: str):
        match self._api_service:
            case 'GoogleTranslator':
                return self._translator.translate(text)
            case 'DeepLTranslator':
                return self._translator.translate(text)
            case _:
                return self._translator.translate(text)
