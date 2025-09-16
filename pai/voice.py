"""Voice interface for the Personal AI Infrastructure."""

from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path
from typing import Optional

from server import PAIClient

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


def _install_file_handler() -> None:
    """Write voice interaction logs under pai/logs/."""

    home = Path(os.getenv("PAI_HOME", Path(__file__).resolve().parent))
    log_dir = home / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_dir / "voice.log")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    LOGGER.addHandler(handler)


def _check_dependency(module_name: str) -> bool:
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def check_dependencies() -> dict[str, bool]:
    return {
        "speech_recognition": _check_dependency("speech_recognition"),
        "pyttsx3": _check_dependency("pyttsx3"),
        "pyaudio": _check_dependency("pyaudio"),
    }


def ensure_dependencies() -> None:
    missing = [name for name, ok in check_dependencies().items() if not ok]
    if missing:
        instructions = "\n".join(
            f"- pip install {name}" for name in missing
        )
        raise SystemExit(
            "Missing voice dependencies:\n"
            f"{instructions}\n"
            "Run this script again after installing the required packages."
        )


def interact(
    client: PAIClient,
    *,
    audio_file: Optional[Path] = None,
    mute: bool = False,
) -> None:
    import speech_recognition as sr  # type: ignore
    import pyttsx3  # type: ignore

    recognizer = sr.Recognizer()
    engine = None if mute else pyttsx3.init()

    audio_data: Optional[sr.AudioData]
    if audio_file:
        path = Path(audio_file)
        if not path.exists():
            LOGGER.error("Audio file not found: %s", path)
            return
        with sr.AudioFile(str(path)) as source:
            LOGGER.info("Loading audio file: %s", path)
            audio_data = recognizer.record(source)
    else:
        try:
            with sr.Microphone() as source:
                LOGGER.info("Listening for voice input")
                audio_data = recognizer.listen(source)
        except OSError as exc:
            LOGGER.error("Audio input unavailable: %s", exc)
            return

    try:
        text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        LOGGER.error("Could not understand audio input")
        return
    except sr.RequestError as exc:
        LOGGER.error("Speech recognition request failed: %s", exc)
        return

    LOGGER.info("Transcribed input: %s", text)
    response = client.chat(text)
    if not response.get("choices"):
        LOGGER.warning("No response choices returned")
        return
    message = response["choices"][0]["message"]["content"]
    if engine is None:
        LOGGER.info("Mute enabled; skipping audio playback")
        return
    try:
        engine.say(message)
        engine.runAndWait()
    except Exception as exc:  # pragma: no cover - runtime guard
        LOGGER.exception("Text-to-speech playback failed: %s", exc)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="PAI Voice Interface")
    parser.add_argument("--check-deps", action="store_true", help="Verify required packages")
    parser.add_argument(
        "--audio-file",
        type=Path,
        help="Use a prerecorded audio file instead of the system microphone.",
    )
    parser.add_argument(
        "--mute",
        action="store_true",
        help="Skip audio playback (useful for automated tests).",
    )
    args = parser.parse_args(argv)

    if args.check_deps:
        results = check_dependencies()
        for name, ok in results.items():
            status = "installed" if ok else "missing"
            print(f"{name}: {status}")
        return 0

    ensure_dependencies()
    if not os.getenv("PAI_HOME"):
        os.environ["PAI_HOME"] = str(os.path.dirname(__file__))
    _install_file_handler()
    client = PAIClient()
    interact(client, audio_file=args.audio_file, mute=args.mute)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
