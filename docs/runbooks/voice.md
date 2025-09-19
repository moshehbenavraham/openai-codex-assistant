# Voice Runbook (In-Chat)

Atlas can run the voice pipeline end-to-end from the Codex CLI chat. Use these
prompts to validate dependencies and smoke tests.

## Dependency Check via Chat

1. Request verification:
   ```text
   Atlas, run pai/voice.py --check-deps and show the formatted output.
   ```
2. Atlas lists the status of `speech_recognition`, `pyttsx3`, and `pyaudio`.
   - If packages are missing in a legacy environment, Atlas will suggest the
     `uv pip install` commands needed to restore them.

## Prerecorded Smoke Test

1. Execute the sample:
   ```text
   Atlas, run pai/voice.py with --audio-file pai/tests/audio/hello.wav --mute and share the log lines.
   ```
2. Atlas should confirm the transcription and note that playback is muted.
3. Ask for the log tail:
   ```text
   Atlas, tail -n 5 pai/logs/voice.log.
   ```

## Live Microphone Test

When hardware is available:

```text
Atlas, start pai/voice.py in live mode so I can speak a short prompt, then report the transcript.
```

Atlas will warn if ALSA/PulseAudio devices are unavailable and surface the exact
error message.

## Troubleshooting Prompts

- `Atlas, run arecord -l so we can confirm the microphone exists.`
- `Atlas, reinstall pyaudio with uv pip if it is missing and document the command.`
- `Atlas, check pai/logs/voice.log for recent ERROR entries.`

## Legacy Commands (Fallback Only)

For detached environments you may run:

```bash
PAI_HOME=$(pwd)/pai PYTHONPATH=pai .venv/bin/python pai/voice.py --check-deps
PAI_HOME=$(pwd)/pai PYTHONPATH=pai .venv/bin/python pai/voice.py --audio-file pai/tests/audio/hello.wav --mute
```

Whenever you use the fallback path, mention it in the changelog and revert to the
in-chat workflow afterward.
