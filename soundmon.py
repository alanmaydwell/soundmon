import pyaudio
import audioop
import time
import matplotlib.pyplot as plt


"""
Measure audio level for period of time

INput source info
https://stackoverflow.com/questions/36894315/how-to-select-a-specific-input-device-with-pyaudio

Based on example from here
https://raspberrypi.stackexchange.com/questions/88641/real-time-sound-level-through-usb-audio-card

ANother example
https://raspberrypi.stackexchange.com/questions/38756/real-time-audio-input-output-in-python-with-pyaudio
"""


def audio_level_monitor(duration=20, chunk=1024, rate=44100, bodge=True):
    """Measure audio level for a fixed period.
    Return results as dictionary with time from start in
    seconds as key and rms of audio chunck as value."""
    results = {}
    audio = pyaudio.PyAudio()

    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

    start_time = time.time()
    for i in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk, exception_on_overflow=False)
        rms = audioop.rms(data, 2)
        now = time.time() - start_time
        # Theres a big spike in the first 0.3 second.
        # Not sure why. This is bodge to remove it!
        if bodge:
            if now < 0.3:
                rms = 128
        results[now] = rms
        print(now, rms)

    stream.stop_stream()
    stream.close()
    audio.terminate()
    return results

def graph(data, title="Graph"):
    """Plot a graph of the data"""
    time.strftime("%d/%m/%Y %H:%M:%S")
    plt.figure(figsize=(7, 6))
    plt.title(title)
    plt.plot(data.keys(), data.values())
    #plt.xticks(x_pos, x_pos)
    plt.ylabel("Sound Level")
    plt.xlabel("Time (s)")
    plt.show()
    
def export(data, filename="data.tsv", heading=""):
    """Export the data to a tsv file"""
    with open(filename, "w") as outfile:
        if heading:
            outfile.write(heading + "\n")
        for key, value in data.items():
            outfile.write(str(key) + "\t" + str(value) + "\n")
                   
    
if __name__ == "__main__":
    date_time = time.strftime("%d/%m/%Y %H:%M:%S")
    filename = time.strftime("sounds_%Y.%m.%d_[%H.%M.%S].tsv")
    results = audio_level_monitor(5)
    graph(results, title=date_time)
    export(results, filename=filename, heading=date_time)