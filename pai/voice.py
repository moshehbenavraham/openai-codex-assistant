"""Voice interface for the Personal AI Infrastructure."""

from __future__ import annotations

import argparse
import logging
import os
from typing import Optional

from server import PAIClient

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


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


def interact(client: PAIClient) -> None:
    import speech_recognition as sr  # type: ignore
    import pyttsx3  # type: ignore

    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

    with sr.Microphone() as source:
        LOGGER.info("Listening for voice input")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
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
    engine.say(message)
    engine.runAndWait()


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="PAI Voice Interface")
    parser.add_argument("--check-deps", action="store_true", help="Verify required packages")
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
    client = PAIClient()
    interact(client)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
