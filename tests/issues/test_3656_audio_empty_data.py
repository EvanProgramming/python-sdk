import pytest

from mcp.server.mcpserver.utilities.types import Audio, Image


def test_image_accepts_empty_data():
    # Documented baseline: Image already accepted empty bytes.
    img = Image(data=b"")
    assert img.data == b""
    assert img.path is None


def test_audio_accepts_empty_data():
    # Regression for #3656: empty bytes are a valid (zero-length) payload,
    # but Audio rejected them because it used `bool(data)` truthiness while
    # Image used `is None` semantics (so `Audio(data=b"")` raised and
    # `Image(data=b"")` did not — same API, different behavior).
    audio = Audio(data=b"")
    assert audio.data == b""
    assert audio.path is None


def test_audio_requires_path_or_data():
    with pytest.raises(ValueError):
        Audio()


def test_audio_rejects_both_path_and_data():
    with pytest.raises(ValueError):
        Audio(path="x", data=b"x")


def test_audio_accepts_path_only():
    audio = Audio(path="sound.wav")
    assert audio.path is not None
    assert audio.data is None


def test_audio_accepts_data_only():
    audio = Audio(data=b"abc")
    assert audio.data == b"abc"
    assert audio.path is None
