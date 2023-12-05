from pydub import AudioSegment
import subprocess
import math
import cv2
import os

offset = 50

def get_audio_duration(audio_file):
    return len(AudioSegment.from_file(audio_file))

def write_text(text, frame, video_writer):
    font = cv2.FONT_HERSHEY_SIMPLEX
    white_color = (255, 255, 255)
    black_color = (0, 0, 0)
    thickness = 10
    font_scale = 3
    border = 5

    # Calculate the position for centered text
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2  # Center horizontally
    text_y = (frame.shape[0] + text_size[1]) // 2  # Center vertically
    org = (text_x, text_y)  # Position of the text

    frame = cv2.putText(frame, text, org, font, font_scale, black_color, thickness + border * 2, cv2.LINE_AA)
    frame = cv2.putText(frame, text, org, font, font_scale, white_color, thickness, cv2.LINE_AA)

    video_writer.write(frame)

def add_narration_to_video(narrations, input_video, output_dir, output_file):
    # Open the video file
    cap = cv2.VideoCapture(input_video)

    # Define the codec and create a VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    temp_video = os.path.join(output_dir, "with_transcript.avi")
    out = cv2.VideoWriter(temp_video, fourcc, 30, (int(cap.get(3)), int(cap.get(4))))

    full_narration = AudioSegment.empty()

    for i, narration in enumerate(narrations):
        audio = os.path.join(output_dir, "narrations", f"narration_{i+1}.mp3")
        duration = get_audio_duration(audio)
        narration_frames = math.floor(duration / 1000 * 30)

        full_narration += AudioSegment.from_file(audio)

        char_count = len(narration.replace(" ", ""))
        ms_per_char = duration / char_count

        frames_written = 0
        words = narration.split(" ")
        for w, word in enumerate(words):
            word_ms = len(word) * ms_per_char

            if i == 0 and w == 0:
                word_ms -= offset
                if word_ms < 0:
                    word_ms = 0

            for _ in range(math.floor(word_ms/1000*30)):
                ret, frame = cap.read()
                if not ret:
                    break
                write_text(word, frame, out)
                frames_written += 1

        for _ in range(narration_frames - frames_written):
            ret, frame = cap.read()
            out.write(frame)

    while out.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    temp_narration = os.path.join(output_dir, "narration.mp3")
    full_narration.export(temp_narration, format="mp3")

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()

    # Close all OpenCV windows (if any)
    cv2.destroyAllWindows()

    ffmpeg_command = [
        'ffmpeg',
        '-y',
        '-i', temp_video,
        '-i', temp_narration,
        '-map', '0:v',   # Map video from the first input
        '-map', '1:a',   # Map audio from the second input
        '-c:v', 'copy',  # Copy video codec
        '-c:a', 'aac',   # AAC audio codec
        '-strict', 'experimental',
        os.path.join(output_dir, output_file)
    ]

    subprocess.run(ffmpeg_command, capture_output=True)

    os.remove(temp_video)
    os.remove(temp_narration)
