import pytest

pytest.importorskip("selenium")
pytest.importorskip("pynput")

from typewriterbot.bot import exit_with_message


def test_exit_success():
    with pytest.raises(SystemExit) as exc:
        exit_with_message(False, "ok")
    assert exc.value.code == 0


def test_exit_error():
    with pytest.raises(SystemExit) as exc:
        exit_with_message(True, "bad")
    assert exc.value.code == 1
