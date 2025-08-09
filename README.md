<img width="3188" height="1202" alt="frame (3)" src="https://github.com/user-attachments/assets/517ad8e9-ad22-457d-9538-a9e62d137cd7" />


# Kayyi Adikeda!!! 🎯


## Basic Details
### Team Name: Cipher


### Team Members
- Team Lead: Aaron Verghese Shaji - College Of Engineering Munnar
- Member 2: Rixon N Punnachan - College Of Engineering Munnar


### Project Description
My project build is a program for switching ON/OFF a light bulb by clap detection. By clapping one time,switches on the bulb; two clap allows you to turn it off ,and three clap goes into party mode and plays a corny music.


### The Problem (that doesn't exist)
When we get into our room,its dark which makes it hard to find the light switch but could be turned ON with a clap and OFF.While we lie down to sleep and forget to turned the lights off, its a disaster right!!This issue can be solved with just one clap.If u wanna make put a party mode,this can be done with just three claps.

### The Solution (that nobody asked for)

This could be used for real world use with a light bulb with right hardwares and changes to the code to implement it which makes it easy to switch on bulb and off with a clap.Mood for a party, 3 claps and the party is on!!!!

## Technical Details
### Technologies/Components Used
For Software:
- Python
- Tkinter
- sounddevice,scipy.signal,numpy,pygame,pyttsx3
- Audio input, signal processing, pattern detection 





### Project Documentation
For Software:

# Screenshots (Add at least 3)
<img width="1757" height="694" alt="Kayyi adikeda!!!_code" src="https://github.com/user-attachments/assets/53245900-5217-4ca6-880d-8a708900b681" />
This shows the code.

<img width="1892" height="964" alt="Kayyi adikeda_terminal to run" src="https://github.com/user-attachments/assets/4dbb97cd-ef8f-46b7-9c0e-b5a90fae2b5a" />
This shows the code with the terminal for run.

<img width="1909" height="1019" alt="Kayyi adikeda_with run and GUI" src="https://github.com/user-attachments/assets/d6a40014-774d-44a0-8fe2-1c404d341bb4" />
This shows how it runs and the gui it shows as a prototype.

# Diagrams
                ┌───────────────────┐
                │ Microphone Input   │
                └───────┬───────────┘
                        │ (sounddevice stream)
                        ▼
             ┌──────────────────────────┐
             │ Audio Processing Pipeline │
             │ - Bandpass filter         │
             │ - RMS & peak detection    │
             │ - Dynamic noise threshold │
             └───────────┬──────────────┘
                         │ (detected clap)
                         ▼
                ┌─────────────────┐
                │ Clap Queue       │
                │ (time-stamped)   │
                └─────────┬───────┘
                          │
                          ▼
            ┌────────────────────────┐
            │ Sequence Processor      │
            │ - Count claps           │
            │ - Timeout after gap     │
            └───────────┬────────────┘
                        │
                        ▼
           ┌───────────────────────────────┐
           │ Action Handler                 │
           │ - Light ON / OFF / Party mode  │
           │ - Random ignore mode           │
           │ - TTS responses                │
           └────────────────┬──────────────┘
                            │
      ┌─────────────────────┼───────────────────────┐
      ▼                     ▼                       ▼
GUI Update            Music Control         Voice Feedback
(Tkinter bulb)        (pygame mixer)        (pyttsx3 TTS)



### Project Demo
# Video
https://drive.google.com/drive/folders/1rdWEg-2WMQMwIvwenC5yUAtfRsQIcVxj?usp=sharing
This video demo shows how the protoype works with clap sequences,
1 clap- Turns ON
2 clap- Turns OFF
3 clap- Turns the party mode ON




## Team Contributions
- Aaron Verghese Shaji: Idea and Program code.
- Rixon N Punnachan: Helped with code development and training sequences.


---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--25-25?link=https%3A%2F%2Fwww.tinkerhub.org%2Fevents%2FQ2Q1TQKX6Q%2FUseless%2520Projects)



