import sys
import os

initial_file = ""
num_iterations = 0
video_codecs = []
audio_codec = "copy"

if len(sys.argv) < 4 or len(sys.argv) > 5:
    print("Usage python <initial-file> <num-iterations> <video-codec1[,videocodec2,[...]]> [audio codec]")
    exit()

initial_file = sys.argv[1]

try:
    num_iterations = int(sys.argv[2])
except ValueError:
    print("Invalid number of iterations \"{}\"".format(sys.argv[2]))
    exit()

video_codecs = [codec.strip() for codec in sys.argv[3].split(",")]

if len(sys.argv) == 5:
    audio_codec = sys.argv[5]

if not os.path.exists("output"):
    os.mkdir("output")

for video_codec in video_codecs:
    if not os.path.exists("output/" + video_codec):
        os.mkdir("output/" + video_codec)
        
    run_number = 0
    contents = os.listdir("output/" + video_codec)
    if not len(contents) == 0:
        run_number = int(sorted(contents, reverse=True)[0])

    out_dir = "output/{}/{}/".format(video_codec, run_number)
    os.mkdir(out_dir)

    for i in range(num_iterations):
        input_file = ""
        output_file = "{}-{}.mkv".format(video_codec, i)

        if i == 0:
            input_file = initial_file
        else:
            input_file = out_dir + "{}-{}.mkv".format(video_codec, i - 1)

        command = "ffmpeg -i {} -c:v {} -c:a {} {}".format(input_file, video_codec, audio_codec, out_dir + output_file)
        