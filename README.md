# Shortrocity

Shortrocity is a tool for making AI generated short videos ("shorts" or "reels") with a ChatGPT generated script, narrated by ElevenLabs or OpenAI text-to-speech. DALL-E 3 generated background images are also added to the background.

## Quick Start

First, add your API-keys to the environment:

```console
$ export OPENAI_API_KEY=YOUR_OPENAI_API_KEY
$ export ELEVENLABS_API_KEY=YOUR_ELEVENLABS_API_KEY
```

Then, put your source content in a file, for example `source.txt` and run the `main.py`:

```console
$ ./main.py source.txt
Generating script...
Generating narration...
Generating images...
Generating video...
DONE! Here's your video: shorts/1701788183/short.avi
``````
