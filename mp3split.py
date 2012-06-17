__author__ = 'Max Morozov'
import os
import re
import wave
import sys
from subprocess import call

class Splitter:
    def make_wav(self):
        try:
            src_path = sys.argv[1]
            self.number = int(re.search('(\d+)', src_path).group(0))
            self.dir_path = re.split('[^\\\\]+$', src_path)[0]
            self.wav_path = "{:s}rt_podcast{:d}.wav".format(self.dir_path, self.number)
            if not os.path.exists(self.wav_path):
                call(["lame.exe", "-S", "--decode",  src_path, self.wav_path])
        except IndexError:
            print "Usage: mp3split <filename>"

    def split(self):
        new_dir = self.dir_path + "rt" + str(self.number)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        wr = wave.open(self.wav_path)
        params = wr.getparams()
        frame_cnt = wr.getnframes()
        r = 0
        frames_per_file = wr.getframerate() * 60 * 5
        frames_wrote = 0
        while frames_wrote < frame_cnt:
            wr.setpos(frames_wrote)
            frames = wr.readframes(frames_per_file)#5 minutes
            tail = frames[-200000:] #searching for ~44100 * 2 channels * 2 seconds  of "zeroes"
            i = 0
            silence = 0
            while i < len(tail):
                v = ord(tail[i]) + 256 * ord(tail[i + 1])
                if v < 40000:#threshold
                    silence += 1
                    if silence > 500:
                        break
                else:
                    if silence:
                        silence = 0
                i += 2
            if frame_cnt - frames_wrote <= silence:
                break
            if silence > 500:
                frames = frames[:-(2 * silence)]
            rt_path = "{:s}/rt{:d}.wav".format(new_dir, r)
            ww = wave.open(rt_path, "wb")
            ww.setparams(params)
            ww.writeframes(frames)
            ww.close()
            call(["lame.exe", "-S", "--ta", "Radio-T", "--tl", "Radio-T " + str(self.number), "--tt", "track#{:02d}".format(r), "--tn", str(r),  rt_path, "{:s}/rt{:02d}.mp3".format(new_dir, r)])
            os.remove(rt_path)
            frames_wrote += len(frames)/2 #one frame = 2 bytes
            r += 1
        wr.close()
        os.remove(self.wav_path)

def main():
    split = Splitter()
    split.make_wav()
    split.split()
main()