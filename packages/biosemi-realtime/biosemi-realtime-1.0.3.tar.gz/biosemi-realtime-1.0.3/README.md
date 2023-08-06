# Real-time Biosemi averager 
This is a realtime interface to assess EEG recordings while recording. 
The interface worksalong side with ActiveView by means of TCP communication.
In order to receive data, ActiveView and biosemi_real_time must match the 
TCP configuration (e.g. Channels being sent, triggers, etc).
The interface allows to obtain real-time estimations of SNR in the time and 
frequency domain. 

## Installation
This software requires Python >= 3.9

Standard installation of stable release can be obtained from the official repository 
```commandline
pip install biosemi-realtime
```

# For Windows
Precompiled PyFFTW is easier to install via conda.
If you are using window, this is the easiest way to have PyFFT running.

```commandline
conda install -c conda-forge pyfftw
```


# Executable
To create an executable you can edit the real_time_app.spec according to your 
needs.
You will also need to install pyinstaller in your system.
Afterwards run following code 
- pyinstaller real_time_app.spec


# Screenshots 

## Incoming data
![](./screenshots/Screenshot_1.png)

## Average data
![](./screenshots/Screenshot_2.png)

## Electrically evoked auditory brainstem response (eABR) recorded from a human participant.
![](./screenshots/Screenshot_eABR.png)
![](./screenshots/Screenshot_eABR_2.png)
