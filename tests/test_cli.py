import pytest

pytest.importorskip('selenium')
pytest.importorskip('pynput')

from typewriterbot.cli import parse_args


def test_parse_login_args():
    args = parse_args(['--browser', 'c', '--speed', '300', 'login'])
    assert args.browser == 'c'
    assert args.speed == 300
    assert args.command == 'login'
    assert args.times == 1


def test_parse_exercise_args():
    url = 'https://example.com'
    args = parse_args(['--browser', 'f', '--speed', '250', 'exercise', url])
    assert args.browser == 'f'
    assert args.command == 'exercise'
    assert args.url == url
