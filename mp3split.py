__author__ = 'mmorozov'
import os
import re
import wave
import sys
from subprocess import call

class Splitter:
    def make_wav(self):
        try:
            srcpath = sys.argv[1]
            self.number = int(re.search('(\d+)', srcpath).group(0))
            self.dirpath = re.split('[^\\\\]+$', srcpath)[0]
            self.wavpath = "%(p)srt_podcast%(n)d.wav" % {"p" : self.dirpath, "n" : self.number}
            if not os.path.exists(self.wavpath):
                call(["lame.exe", "-S", "--decode",  srcpath, self.wavpath])
        except IndexError:
            print "Usage: mp3split <filename>"

    def split(self):
        new_dir = self.dirpath + "rt" + str(self.number)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        wr = wave.open(self.wavpath)
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
            rtpath = "%(path)s/rt%(idx)d.wav" % {"path": new_dir, "idx": r}
            ww = wave.open(rtpath, "wb")
            ww.setparams(params)
            ww.writeframes(frames)
            ww.close()
            call(["lame.exe", "-S", "--ta", "Radio-T", "--tl", "Radio-T" + str(self.number), "--tt", "track#{:02d}".format(r), "--tn", str(r),  rtpath, "{:s}/rt{:02d}.mp3".format(new_dir, r)])
            os.remove(rtpath)
            frames_wrote += len(frames)/2 #one frame = 2 bytes
            r += 1
        wr.close()
        os.remove(self.wavpath)

def main():
    split = Splitter()
    split.make_wav()
    split.split()
main()