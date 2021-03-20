import os
import time

def main():
    if not os.path.exists("crf_tests"):
        os.mkdir("crf_tests")
        
    times_csv = open("crf_tests/times.csv", "w")
    times_csv.write("CRF,Time\n")

    for i in range(0, 51):
        print("CRF {}:".format(i + 1), end = "")

        command = "ffmpeg -hide_banner -loglevel error -i oceans.mp4 -c:v libx264 -c:a copy -crf {} crf-{}.mp4".format(i + 1, i + 1)

        start_time = time.perf_counter()
        os.system(command)
        end_time = time.perf_counter()

        times_csv.write("{},{}\n".format(i + 1, end_time - start_time))

        print("Done")

    times_csv.close()


if __name__ == "__main__":
    main()