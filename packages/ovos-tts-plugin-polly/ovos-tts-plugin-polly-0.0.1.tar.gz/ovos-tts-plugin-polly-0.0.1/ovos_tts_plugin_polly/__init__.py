import logging

import boto3
from ovos_plugin_manager.templates.tts import TTS, TTSValidator

logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('urllib3.util.retry').setLevel(logging.CRITICAL)


class PollyTTS(TTS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, audio_ext="mp3",
                         validator=PollyTTSValidator(self))
        # Catch Chinese alt code
        if self.lang.lower() == "zh-zh":
            self.lang = "cmn-cn"
        self.ssml_tags = ["speak", "say-as", "voice",
                          "prosody", "break",
                          "emphasis", "sub", "lang",
                          "phoneme", "w", "whisper",
                          "amazon:auto-breaths",
                          "p", "s", "amazon:effect",
                          "mark"]
        self.voice = self.config.get("voice", "Matthew")
        self.key_id = self.config.get("key_id") or \
                      self.config.get("access_key_id") or ""
        self.key = self.config.get("secret_key") or \
                   self.config.get("secret_access_key") or ""
        self.region = self.config.get("region", 'us-east-1')
        self.polly = boto3.Session(aws_access_key_id=self.key_id,
                                   aws_secret_access_key=self.key,
                                   region_name=self.region).client('polly')

    def get_tts(self, sentence, wav_file):
        text_type = "text"
        if self.remove_ssml(sentence) != sentence:
            text_type = "ssml"
            sentence = sentence.replace("\whispered", "/amazon:effect") \
                .replace("\\whispered", "/amazon:effect") \
                .replace("whispered", "amazon:effect name=\"whispered\"")
        response = self.polly.synthesize_speech(
            OutputFormat=self.audio_ext,
            Text=sentence,
            TextType=text_type,
            VoiceId=self.voice.title())

        with open(wav_file, 'wb') as f:
            f.write(response['AudioStream'].read())
        return wav_file, None

    def describe_voices(self, language_code="en-US"):
        if language_code.islower():
            a, b = language_code.split("-")
            b = b.upper()
            language_code = "-".join([a, b])
        # example 'it-IT' useful to retrieve voices
        voices = self.polly.describe_voices(LanguageCode=language_code)

        return voices


class PollyTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(PollyTTSValidator, self).__init__(tts)

    def validate_lang(self):
        # TODO
        pass

    def validate_dependencies(self):
        try:
            from boto3 import Session
        except ImportError:
            raise Exception(
                'PollyTTS dependencies not installed, please run pip install '
                'boto3 ')

    def validate_connection(self):
        try:
            if not self.tts.voice:
                raise Exception("Polly TTS Voice not configured")
            output = self.tts.describe_voices()
        except TypeError:
            raise Exception(
                'PollyTTS server could not be verified. Please check your '
                'internet connection and credentials.')

    def get_tts_class(self):
        return PollyTTS


if __name__ == "__main__":
    e = PollyTTS(config={"key_id": "",
                         "secret_key": ""})

    ssml = """<speak>
     This is my original voice, without any modifications. <amazon:effect vocal-tract-length="+15%"> 
     Now, imagine that I am much bigger. </amazon:effect> <amazon:effect vocal-tract-length="-15%"> 
     Or, perhaps you prefer my voice when I'm very small. </amazon:effect> You can also control the 
     timbre of my voice by making minor adjustments. <amazon:effect vocal-tract-length="+10%"> 
     For example, by making me sound just a little bigger. </amazon:effect><amazon:effect 
     vocal-tract-length="-10%"> Or, making me sound only somewhat smaller. </amazon:effect> 
</speak>"""
    e.get_tts(ssml, "polly.mp3")
