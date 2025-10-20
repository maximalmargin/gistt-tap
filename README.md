# gistt

> "Don't confuse motion with progress." Spend less time on email and get more done.

gistt is a terminal-native AI email client that shows you the gist — so you can focus on real progress.

> "tab tab tab for emails."

![gistt CLI walkthrough](media/gistt-demo.gif)

## Why gistt?

Email is broken. Subject lines were supposed to tell you what a message is about, but in a world of promotions they're designed to make you click rather than inform. We haven't rethought the function of email in a while.

gistt is built around three core principles:

1. **Gist-focused, not email-focused** — We show you the gist, not the inbox.
2. **Terminal constraint as a feature** — Minimal UI, forced simplification.
3. **Action-focused state machine** — Get you out as fast as possible (disengagement as success).

## Quick start

### Install via Homebrew (beta)

```bash
brew tap maximalmargin/gistt https://github.com/maximalmargin/gistt-tap
brew install gistt
```

### Prerequisites

- Python 3.10+
- Gmail account
- Google Cloud project with Gmail API enabled
- Gemini API key

### 1. Google Cloud & Gmail API

Enable the Gmail API in your Google Cloud project and download the OAuth client JSON.

- Set application type to 'Desktop app'.
- Add the accounts you want to link to `APIs & Services → OAuth consent screen → Test users`.

### 2. Place credentials

Place the file at `~/.config/gistt/client_secret.json`.

Set the `GISTT_CLIENT_CREDENTIALS` environment variable to override if you prefer a different location.

### 3. Authenticate

Run `gistt` once to complete the OAuth flow.

By default tokens are written to `~/.local/share/gistt/accounts/<email>/token.json`.

**To unlink an account**: Remove the account's folder under `~/.local/share/gistt/accounts/<email>/`.

### 4. Configure Gemini

Set the Gemini API key in your environment (e.g. `.env`):

```bash
# Get your key from https://aistudio.google.com/apikey
export GEMINI_API_KEY="YOUR_API_KEY"
```

**Note**: The CLI stores persisted state under `~/.local/share/gistt`. Remove that directory if you need a clean slate.
There is no database for this application. We don't store anything.

## Usage

After installing via Homebrew, launch the client from any terminal:

```bash
gistt
```

**Keyboard shortcuts**:

- `g` — Fetch new gistts
- `tab` — Execute recommended action
- `s` — Mark as read
- `e` — Archive
- `r` — Draft reply
- `j/k` — Navigate
- `h` — Toggle filter
- `q` — Quit

Customization: On first run `gistt` writes a copy of the packaged defaults to `~/.config/gistt/settings.json` so you can tweak preferences. You can modify the rules and conditions to your liking.
Cached summaries include the action group priority as it existed when they were generated; if you change priorities, run `rm ~/.local/share/gistt/gistt_cache.json` to rebuild with the new ordering.

## Contributing

gistt is early-stage and designed to be hackable. We're looking for tinkerers to help shape it. Here are features we'd love your help with:

- Smoothing out the UI/UX
- Hit `u` to unsubscribe from mailing lists
- Slash commands for power users
- More AI model backends

Email <maximalmargin@gmail.com> to ask about contributing. PRs welcome.

## Inspirations

- [AI Horseless Carriages](https://koomen.dev/essays/horseless-carriages/) by Pete Koomen
- Claude Code, Codex CLI, and Gemini CLI
- [Google's mission](https://www.google.com/intl/en_us/search/howsearchworks/our-approach/) is to organize the world's information and make it universally accessible and useful
- [AI Written, AI Read](https://marketoonist.com/2023/03/ai-written-ai-read.html)
- Squid Game
- Hilma af Klint
- Ready Player One

## Artifact Preview

[View the interactive artifact](https://htmlpreview.github.io/?https://raw.githubusercontent.com/maximalmargin/gistt-tap/main/media/artifact.html)

![Artifact preview](media/artifact-preview.png)
