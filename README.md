# WRTS Account Tools

This project provides tools for generating and managing WRTS/StudyGo accounts.

## Files

- `gen.py`  
  Generate new accounts and save them to `accounts.txt`.

- `src/joiner.py`  
  Functions to join groups with accounts.

- `src/leaver.py`  
  Functions to leave groups with accounts.

- `src/tokenchecker.py`  
  Check if account tokens are valid.

- `src/captcha.py`  
  Solve captchas using CapMonster.

- `accounts.txt`  
  Stores generated account credentials.

## Usage

1. Make sure you have Python 3 and the `requests` library installed.
2. Run `gen.py` to generate accounts.
3. Use the scripts in `src/` to join/leave groups or check tokens.
4. Place your CapMonster API key in the scripts if required.

All scripts use `accounts.txt` for account data.