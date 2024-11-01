# WAB

## Description

**W**ordle **A**uto **B**ackup is a simple script that uses [Selenium](https://www.selenium.dev/) to open a browser with [Wordle](https://lapalabradeldia.com/) and allows you to play and save the backup automatically.

Why I created this project? There are two main reasons, the first one is **for fun**, and the second one because I got tired of doing the backups myself.

>[!NOTE]
>
> Right now it's only supposed to work only on my current machine which has Ubuntu 24.04, but I'll test on different platforms.

## Requirements

- python3
- selenium
- pip
- python3-venv

## Usage

```shell
git clone https://github.com/SrVariable/WAB.git
cd WAB
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
deactivate
```

Once you guessed the word or run out of attempts, you have to go to the terminal and type `quit` or `-q`.

## Features

- Automatically reject data/vendor consents.
- You can play on the terminal
- Load/Save backups
