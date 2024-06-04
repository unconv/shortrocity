# Shortrocity

Shortrocity is a tool for making AI generated short videos ("shorts" or "reels") with a ChatGPT generated script, narrated by ElevenLabs or OpenAI text-to-speech. DALL-E 3 generated background images are also added to the background. Captions with word highlighting are generated with [Captacity](https://github.com/unconv/captacity), which uses [OpenAI Whisper](https://github.com/openai/whisper).

## Quick Start

First, add your API-keys to the environment:

```console
$ export OPENAI_API_KEY=YOUR_OPENAI_API_KEY
$ export ELEVEN_API_KEY=YOUR_ELEVENLABS_API_KEY
```

Then, put your source content in a file, for example `source.txt` and run the `main.py`:

```console
$ ./main.py source.txt
Generating script...
Generating narration...
Generating images...
Generating video...
DONE! Here's your video: shorts/1701788183/short.avi
```

## Caption styling

Optionally, you can specify a settings file to define settings for the caption styling:

```console
$ ./main.py source.txt settings.json
```

The settings file can look like this, for example:

```json
{
    "font": "Bangers-Regular.ttf",
    "font_size": 130,
    "font_color": "yellow",

    "stroke_width": 3,
    "stroke_color": "black",

    "highlight_current_word": true,
    "word_highlight_color": "red",

    "line_count": 2,

    "padding": 50,

    "shadow_strength": 1.0,
    "shadow_blur": 0.1
}
```
