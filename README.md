# TypeWriterBot

Automates typing exercises on [TypeWriter](https://at4.typewriter.at/) using Selenium.

## Installation

1. Install Python 3.8+ and [pip](https://pip.pypa.io/en/stable/).
2. Install runtime dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Usage

The CLI is available as a module or console script.

### Run exercises after login

Set the environment variables `TWB_USERNAME` and `TWB_PASSWORD` and run:

```bash
python -m typewriterbot --browser c --speed 300 login --times 2
```

### Run a single exercise by URL

```bash
python -m typewriterbot --browser f --speed 250 exercise https://example.com/exercise
```

Supported browsers: Firefox (`f`), Chrome (`c`), and Edge (`e`).

## Development

Format and lint the codebase using [pre-commit](https://pre-commit.com/):

```bash
pre-commit run --files typewriterbot/bot.py typewriterbot/cli.py
```

Run the tests with [pytest](https://pytest.org/):

```bash
pytest
```
