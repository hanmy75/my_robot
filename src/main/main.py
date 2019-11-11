#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google Assistant GRPC recognizer."""

import time
import logging
import threading
import snowboydecoder
from ht16k33 import matrix
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from aiy.assistant.grpc import AssistantServiceClientWithSoundClip
from aiy.voice.audio import play_wav

# Define
HOST_PORT = 8080
HOTWORD_MODEL = "resources/hotword.pmdl"
WAKEUP_CLIP = "resources/ding.wav"
END_CLIP    = "resources/dong.wav"


# For Web service
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


###################################
# For Web control
###################################
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('pos')
def program_pos(msx, msy):
    logging.info("pos %d,%d", msx, msy)

@socketio.on('light')
def program_light(flag):
    logging.info("light flag %d", flag)

@socketio.on('cam')
def program_cam(flag):
    logging.info("cam flag %d", flag)

@socketio.on('power')
def program_power(flag):
    logging.info("power flag %d", flag)

@socketio.on('disconnect')
def program_disconnect():
    logging.info("disconnect")


###################################
# For home assistant
###################################
def detected_callback():
    logging.info('Hotword is detected.')
    detector.terminate()

def state_change_callback(input_word):
    logging.info('Conversation state is changed. <%s>', input_word)


###################################
# Sound Clip class
###################################
class SoundClip():
    def __init__(self):
        # Play sound clip
        self._play_wav = play_wav

        # Matrix LED
        self._matrix = matrix.Matrix16x8(address=0x70)
        self._matrix.brightness = 4

    def playWelcome(self):
        self._matrix.putChar('O', 'O')
        self._play_wav(END_CLIP)
        time.sleep(1)
        self._play_wav(END_CLIP)

    def playWakeword(self):
        self._matrix.putChar('?', '?')
        self._play_wav(WAKEUP_CLIP)

    def playEndword(self):
        self._matrix.putChar('!', '!')
        #self._play_wav(END_CLIP)

    def playNormalmode(self):
        self._matrix.putChar('O', 'O')


###################################
# Home assistant thread
###################################
def homeassistantThread():
    logging.info('Start Home assistant thread.')

    while True:
        # start hotword detection
        detector.start(detected_callback)

        # Start conversation
        assistant.conversation(on_state_change=state_change_callback)


###################################
# Main
###################################
if __name__ == '__main__':
    # Set log level
    logging.basicConfig(level=logging.DEBUG)

    # Hotword Detection(snowboy) resource
    detector = snowboydecoder.HotwordDetector(HOTWORD_MODEL, sensitivity=0.5, audio_gain=1.0)

    # Get Board for Home assistant
    soundClip = SoundClip()
    assistant = AssistantServiceClientWithSoundClip(soundClip=soundClip, volume_percentage=100, language_code='ko-KR')

    # Start a thread
    server_thread = threading.Thread(target=homeassistantThread)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()

    # Run Web server
    logging.info('Start web server')
    socketio.run(app, host='0.0.0.0', port=HOST_PORT, debug=False, use_reloader=False)

    logging.info('Exit program')
