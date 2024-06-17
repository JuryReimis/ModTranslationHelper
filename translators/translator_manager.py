from deep_translator import GoogleTranslator, DeeplTranslator, YandexTranslator
from deep_translator.exceptions import InvalidSourceOrTargetLanguage, LanguageNotSupportedException
from deepl import AuthorizationException
from loguru import logger
import deepl


class TranslatorManager:

    supported_apis = [
        "GoogleTranslator",
        # "YandexTranslator",
        "DeepLTranslator"
    ]
    source_for_deepl = None
    target_for_deepl = None

    def __init__(
            self,
            source_language='english',
            target_language='russian',
            api_service=None,
            api_key=None,
    ):
        self._translator: GoogleTranslator | YandexTranslator | deepl.Translator | None = None
        self._source_language = source_language
        self._target_language = target_language
        self._api_service = api_service
        self._api_key = api_key

        self._init_translator_obj()

    @logger.catch()
    def _init_supported_languages(self):
        match self._api_service:
            case 'GoogleTranslator':
                self.source_supported_languages = self.target_supported_languages = GoogleTranslator().get_supported_languages(as_dict=True)
            case 'DeepLTranslator':
                self._translator: deepl.Translator
                self.source_supported_languages = {language.name: language.code.lower() for language in self._translator.get_source_languages()}
                self.target_supported_languages = {language.name: language.code.lower() for language in self._translator.get_target_languages()}
            # case 'YandexTranslator':
            #     self.source_supported_languages = self.target_supported_languages = YandexTranslator(api_key='api_key').get_supported_languages(as_dict=True)

    @logger.catch()
    def check_same_language_codes(self, last_source_code, last_target_code):
        if last_source_code and last_target_code:
            for name, code in self.source_supported_languages.items():
                if last_source_code == code:
                    self._source_language = name
            for name, code in self.target_supported_languages.items():
                if last_target_code == code:
                    self._target_language = name

    @logger.catch()
    def _init_translator_obj(self, last_source_code=None, last_target_code=None):
        try:
            match self._api_service:
                case 'GoogleTranslator':
                    self._init_supported_languages()
                    self.check_same_language_codes(last_source_code, last_target_code)
                    source_language = self.source_supported_languages.get(self._source_language)
                    target_language = self.target_supported_languages.get(self._target_language)
                    self._translator = GoogleTranslator(source=source_language,
                                                        target=target_language)
                case 'DeepLTranslator':
                    self._translator = deepl.Translator(auth_key=self._api_key)
                    self._translator.get_usage()
                    self._init_supported_languages()
                    self.check_same_language_codes(last_source_code, last_target_code)
                    self.source_for_deepl = self.source_supported_languages.get(self._source_language, 'en')
                    self.target_for_deepl = self.target_supported_languages.get(self._target_language, 'ru')
                # case 'YandexTranslator':
                #     self._init_supported_languages()
                #     self.check_same_language_codes(last_source_code, last_target_code)
                #     source_language = self.source_supported_languages.get(self._source_language)
                #     target_language = self.target_supported_languages.get(self._target_language)
                #     self._translator = YandexTranslator(api_key=self._api_key,
                #                                         source=source_language,
                #                                         target=target_language)
                case _:
                    self._translator = None
        except InvalidSourceOrTargetLanguage as error:
            logger.warning(f'Source {self._source_language} and target {self._target_language} languages {error}')
        except LanguageNotSupportedException:
            logger.warning(
                f'Source {self._source_language} and target {self._target_language} not supported in {self._api_service}')
        except AuthorizationException as error:
            logger.warning(f'AuthorizationException {error}')

    def raise_authorization_exception(self):
        try:
            self._translator.get_usage()
        except AuthorizationException as error:
            return AuthorizationException(str(error))
        except Exception:
            return None

    def set_new_api_service(self, api_service, api_key=None, last_source='english', last_target='russian'):
        self._api_service = api_service
        self._api_key = api_key
        last_source_code = self.source_supported_languages.get(last_source).lower()
        last_target_code = self.target_supported_languages.get(last_target).lower()
        self._init_translator_obj(last_source_code=last_source_code, last_target_code=last_target_code)

    def set_new_source_language(self, new_source: str):
        self._source_language = new_source
        self._init_translator_obj()

    def set_new_target_language(self, new_target: str):
        self._target_language = new_target
        self._init_translator_obj()

    def get_source_language(self):
        return self._source_language

    def get_target_language(self):
        return self._target_language

    def get_source_supported_languages(self):
        return self.source_supported_languages.keys()

    def get_target_supported_languages(self):
        return self.target_supported_languages.keys()

    def get_api_name(self):
        return self._api_service

    @logger.catch()
    def translate(self, text: str):
        match self._api_service:
            case 'GoogleTranslator':
                return self._translator.translate(text)
            case 'DeepLTranslator':
                self._translator: deepl.Translator
                return self._translator.translate_text(text=text,
                                                       source_lang=self.source_for_deepl,
                                                       target_lang=self.target_for_deepl,
                                                       tag_handling='html').text
            case _:
                return self._translator.translate(text)

    def __eq__(self, other):
        if self._api_service == other:
            return True
        else:
            return False
