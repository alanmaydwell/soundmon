# SOUNDMON.PY

A simple tool that measures microphone audio level for a period. Created to
help assess state of heating boiler but noise levels were too high for anything useful!


- Measures audio levels for a fixed duration then captures the results.    
- Has simple graph creation using matplotlib
- Exports to tsv file with elapsed time in seconds vs audio level
- Contains bodge that ignores the first 0.3 seconds as always get a big spike here which seems unrelated to actual sound level.



### Requires

- pyaudio
- matplotlib

### Based on info from below
https://raspberrypi.stackexchange.com/questions/88641/real-time-sound-level-through-usb-audio-card