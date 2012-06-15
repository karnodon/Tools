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
                call(["lame.exe", "--decode",  srcpath, self.wavpath])
            print "WAVEFORM was generated"
        except IndexError:
            print "Usage: mp3split <filename>"

    def split(self):
        print "Making dir"
        new_dir = self.dirpath + "rt" + str(self.number)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        wr = wave.open(self.wavpath)
        params = wr.getparams()
        frame_cnt = wr.getnframes()
        r = 0
        frames_per_file = wr.getframerate() * 60 * 5
        while r * frames_per_file < frame_cnt:
            frames = wr.readframes(frames_per_file)#5 minutes
            rtpath = "%(path)s/rt%(idx)d.wav" % {"path": new_dir, "idx": r}
            ww = wave.open(rtpath, "wb")
            ww.setparams(params)
            ww.writeframes(frames)
            ww.close()
            call(["lame.exe", "--ta", "Radio-T", "--tl", "Radio-T" + str(self.number), "--tt", "track#" + str(r), "--tn", str(r),  rtpath, "%(path)s//rt%(idx)d.mp3" % {"path": new_dir, "idx" : r}])
            os.remove(rtpath)
            r += 1
        wr.close()
        os.remove(self.wavpath)
        print "Done"

def main():
    split = Splitter()
    split.make_wav()
    split.split()
main()