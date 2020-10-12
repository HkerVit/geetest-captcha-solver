import speech_recognition as sr
from pydub import AudioSegment
import requests
import random
import json
import os

class Geetest(object):
    def __init__(self, gt, challengeurl):
        self.gt = gt
        self.callback = 'geetest_' + ''.join(random.choice('1234567890') for _ in range(13))
        self.challenge = requests.get(challengeurl).text.split(';')[0]

    def GetMP3(self):
        r = requests.get(f'https://api-na.geetest.com/gettype.php?gt={self.gt}&callback={self.callback}')
        j = json.loads(r.text[22:][:-1])
        r = requests.get(f'https://api-na.geetest.com/get.php?gt={self.gt}&challenge={self.challenge}&lang=en&type=voice&client_type=web&w=&callback={self.callback}')
        return json.loads(r.text[22:][:-1])

    def GetAnswer(self):
        open('temp.mp3', 'wb').write(requests.get(f'https://static.geetest.com{self.GetMP3()["data"]["new_voice_path"]}').content)
        AudioSegment.from_file('temp.mp3').export('payload.wav', format='wav')
        os.remove('temp.mp3')
        r = sr.Recognizer()
        with sr.AudioFile('payload.wav') as s:
            data = r.record(s)
            raw = r.recognize_google(data)
            answer = ''
            os.remove('payload.wav')
            for char in raw:
                if char.isdigit():
                    answer += char
            return answer

    def GetResponse(self):
        r = requests.get(f'https://api-na.geetest.com/ajax.php?gt={self.gt}&challenge={self.challenge}&a={self.GetAnswer()}&lang=en&callback={self.callback}')
        return json.loads(r.text[22:][:-1])

if __name__ == "__main__":
    print(Geetest().GetResponse())