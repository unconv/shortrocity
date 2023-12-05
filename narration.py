from elevenlabs import generate, set_api_key, save, RateLimitError
import openai
import os

elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")

if elevenlabs_key:
    set_api_key(elevenlabs_key)

narration_api = "elevenlabs" # (or "openai")

def parse(narration):
    data = []
    narrations = []
    lines = narration.split("\n")
    for line in lines:
        if line.startswith('Narrator: '):
            text = line.replace('Narrator: ', '')
            data.append({
                "type": "text",
                "content": text.strip('"'),
            })
            narrations.append(text.strip('"'))
        elif line.startswith('['):
            background = line.strip('[]')
            data.append({
                "type": "image",
                "description": background,
            })
    return data, narrations

def create(data, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    n = 0
    for element in data:
        if element["type"] != "text":
            continue

        n += 1
        output_file = os.path.join(output_folder, f"narration_{n}.mp3")

        if narration_api == "openai":
            audio = openai.audio.speech.create(
                input=element["content"],
                model="tts-1",
                voice="alloy",
            )

            audio.stream_to_file(output_file)
        else:
            audio = generate(
                text=element["content"],
                voice="Michael",
                model="eleven_monolingual_v1"
            )
            save(audio, output_file)
