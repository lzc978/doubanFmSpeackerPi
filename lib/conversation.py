# -*- coding: utf-8-*-
import lib.util
from plugin.bootstrap import Bootstrap

class Conversation(object):
    """
    会话交互
    """
    def __init__(self, robot_name, mic, speaker, active_stt, passive_stt, bootstrap_config):
        self._logger = lib.util.init_logger(__name__)
        self.robot_name = robot_name
        self.mic = mic
        self.speaker = speaker
        self.active_stt = active_stt
        self.passive_stt = passive_stt
        self.bootstrap_config = bootstrap_config
        self.bootstrap = Bootstrap(active_stt, bootstrap_config)

    def handleForever(self):
        self._logger.info("开始和机器人{ %s }会话", self.robot_name)
        while True:
            self._logger.debug("Started to listen kw : %s", self.robot_name)
            threshold, transcribed = self.mic.passiveListen(self.robot_name,
                    transcribe_callback=self.passive_stt.transcribe)
            self._logger.debug("Stop to listen kw : %s", self.robot_name)

            if not transcribed or not threshold:
                self._logger.info("Nothing has been said or transcribed.")
                continue
            self._logger.info("Keyword '%s' has been said!", self.robot_name)

            self._logger.debug("Started to listen actively with threshold: %r", threshold)
            input = self.mic.activeListenToAllOptions(threshold,
                    speak_callback=self.speaker.play,
                    transcribe_callback=self.active_stt.transcribe)
            self._logger.debug("Stopped to listen actively with threshold: %r", threshold)

            if input:
                self._logger.debug("Started to bootstrap asr word to plunins with input: %s", input)
                self.bootstrap.query(input)
            else:
                self.speaker.say("没听清楚，请再说一次")
