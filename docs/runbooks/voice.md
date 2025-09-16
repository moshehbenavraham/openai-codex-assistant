# Voice Runbook

## Prerequisites

- Activate the project virtual environment: `source .venv/bin/activate`.
- Install Python dependencies: `pip install SpeechRecognition pyttsx3`.
- Install system TTS backend (`espeak-ng`) and microphone drivers
  (`portaudio19-dev` provides PyAudio bindings).
- Export `PAI_HOME=$(pwd)/pai` if the workspace lives outside `~/pai`.

## Dependency Check

1. Verify Python packages and surface missing modules:

   ```bash
   PAI_HOME=$(pwd)/pai PYTHONPATH=pai .venv/bin/python pai/voice.py --check-deps
   ```

2. Sample output after installing `SpeechRecognition` and `pyttsx3`:

   ```text
   speech_recognition: installed
   pyttsx3: installed
   pyaudio: installed
   ```

3. If any dependency is missing, install it inside the virtual environment and
   rerun the check.

## First Interactive Test

1. Run the voice interface from the project root:

   ```bash
   PAI_HOME=$(pwd)/pai PYTHONPATH=pai .venv/bin/python pai/voice.py
   ```

2. Expected failure without system TTS backend:

   ```text
   RuntimeError: This means you probably do not have eSpeak or eSpeak-ng installed!
   ```

3. Install `espeak-ng` (and `ffmpeg` if you want alternative voices), then
   rerun the command.
4. For automated tests or sandbox verification, pass a prerecorded sample and
   mute playback:

   ```bash
   PAI_HOME=$(pwd)/pai PYTHONPATH=pai .venv/bin/python pai/voice.py \
     --audio-file pai/tests/audio/hello.wav --mute
   ```

   Sample log output (`pai/logs/voice.log`):

   ```text
   2025-09-16 08:54:48,658 INFO __main__ Loading audio file: pai/tests/audio/hello.wav
   2025-09-16 08:54:53,195 INFO __main__ Transcribed input: hello from PI
   2025-09-16 08:55:08,169 INFO __main__ Mute enabled; skipping audio playback
   ```

5. When hardware is available, speak a short prompt after the "Listening for
   voice input" log line. Successful runs print interaction messages to the
   console, write to `pai/logs/voice.log`, and play synthesized audio via
   `pyttsx3`.
6. Example failure without a default microphone:

   ```text
   Audio input unavailable: No Default Input Device Available
   ```

## Troubleshooting

- If the script exits with `Could not understand audio input`, verify your
  microphone defaults and background noise levels.
- `OSError: No Default Input Device Available` indicates missing ALSA or
  PulseAudio configuration. Confirm the device works via `arecord -l`.
- `ModuleNotFoundError: No module named 'pyaudio'` means you still need to
  install `portaudio19-dev` followed by `pip install pyaudio` within the
  virtual environment.
- After installing system packages, rebuild the virtual environment or
  reinstall affected wheels (`pip install --force-reinstall pyttsx3 pyaudio`).
