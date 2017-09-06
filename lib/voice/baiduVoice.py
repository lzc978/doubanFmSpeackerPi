# -*- coding: utf-8-*-

import sys
import os

import yaml

import lib.diagnose
from baseVoice import AbstractVoiceEngine
import lib.appPath

try:
    from aip import AipSpeech
except ImportError:
    pass

class BaiduVoice(AbstractVoiceEngine):
    """
    Uses the Baidu AI Cloud Services.
    """
    TAG = "baidu-ai"

    def __init__(self, app_id='', api_key='', secret_key='',
            per=0, output_file=os.path.join(lib.appPath.DATA_PATH, 'baidu_voice.mp3')):
        super(self.__class__, self).__init__()
        self._aipSpeech = AipSpeech(app_id, api_key, secret_key)
        self._per = per
        self._output_file = output_file

    @classmethod
    def get_config(cls):
        config = {}
        config_path = os.path.join(lib.appPath.CONFIG_PATH, 'baidu.yml')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                profile = yaml.safe_load(f)
                if 'voice' in profile:
                    voice_config = profile['voice']
                    if 'app_id' in voice_config:
                        config['app_id'] = voice_config['app_id']
                    if 'api_key' in voice_config:
                        config['api_key'] = voice_config['api_key']
                    if 'secret_key' in voice_config:
                        config['secret_key'] = voice_config['secret_key']
                    if 'per' in voice_config:
                        config['per'] = voice_config['per']
                    if 'output_file' in voice_config:
                        config['output_file'] = voice_config['output_file']
        return config

    @classmethod
    def is_available(cls):
        return (super(cls, cls).is_available() and
                diagnose.check_python_import('baidu-aip') and
                diagnose.check_network_connection('www.baidu.com'))

    def say(self, phrase):
        self._logger.debug("Saying '%s' with '%s'", phrase, self.TAG)
        result  = self._aipSpeech.synthesis(phrase, 'zh', 1, { 'per':self._per,'vol': 5, })
        # 识别正确返回语音二进制 错误则返回dict 参照http://yuyin.baidu.com/docs/tts/196 错误码
        if not isinstance(result, dict):
            with open(self._output_file, 'wb') as f:
                f.write(result)
        self.play(self._output_file)
        os.remove(self._output_file)

    def asr(self,record_file=os.path.join(lib.appPath.DATA_PATH,"baidu_record.wav")):
        if os.path.exists(record_file):
            with open(record_file, 'rb') as f:
                records = f.read()
                aipSpeech.asr(records, 'wav', 16000, { 'lan': 'zh', })

