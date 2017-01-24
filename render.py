import os.path, time, sys
from subprocess import call

#command for exporting single frames:
#  ffmpeg -i n.wmv -ss 00:00:20 -t 00:00:1 -s 320x240 -r 1 -f singlejpeg myframe.jpg
fps = 60

File = "videoFile"
OutputFolder = "blank"
cfg = "configFile"
#offset sets the offset in microseconds from the trigger
offset = 0;
metaOffset = 25;
print "created: %s" % time.ctime(os.path.getctime(File))
Toffset = os.path.getctime(File)
commandBegin = {"ffmpeg", "-i", File, "-ss"} #after this the timecode has to be appended
commandEnd   = {"-t", "00:00:1", "-r", "1", "-f", "singlejpeg"} #after this the output file needs to be put

def get_command(timeCode, outPutFile):
    command = list()
    command.append(commandBegin)
    command.append(timeCode)
    command.append(commandEnd)
    command.append(outPutFile)
    return(command)

def getTimecode(frame):
    frame = frame*1000
    frame = frame+offset
    Fstring = str(int(frame))
    print(Fstring)
    microSec = "."+Fstring[-3:] #last 3 digits
    frames = fNum = int(float(microSec)*fps)
    normalSec = Fstring[:-3] #normal seconds
    #now lets get hours
    hours = int(int(normalSec)/3600)
    print("hours:"+str(hours))
    leftoverSec  = int(normalSec)-hours*3600
    minutes = leftoverSec/60
    seconds = leftoverSec-minutes*60

    print("minutes:"+str(minutes))
    print("seconds:"+str(seconds))
    print("frames:"+str(frames))

getTimecode(time.time()-1485183747.98)
exit(0)
#now we need to read the config file
with open(cfg, "r") as cFile:
    Lines = cFile.read().split("\n")
    i = 0
    w = 0
    l = len(Lines)
    for line in Lines:
        Name = ""
        if(i<metaOffset):
            parts = line.split(":")
            if(parts[0]=="Name"):
                Name = parts[1]
        if(i>metaOffset):
            #here is the buffers for metadata that we could put in the file
            frame = float(line)-Toffset+offset
            fName = os.path(OutputFolder, Name+'{:04d}'.format(w)+".jpg")
            call(get_command(getTimecode(frame), fName))
            sys.stdout.write("\r"+str(w)+"/"+str(l)+" frames completed")
            sys.stdout.flush()
            w=w+1;
        i=i+1;

