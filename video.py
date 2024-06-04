from pydub import AudioSegment
import subprocess
import numpy as np
import captacity
import json
import math
import cv2
import os

def get_audio_duration(audio_file):
    return len(AudioSegment.from_file(audio_file))

def add_narration_to_video(narrations, input_video, output_dir, output_file):
    full_narration = AudioSegment.empty()

    for i, _ in enumerate(narrations):
        audio = os.path.join(output_dir, "narrations", f"narration_{i+1}.mp3")
        full_narration += AudioSegment.from_file(audio)

    temp_narration = os.path.join(output_dir, "narration.mp3")
    full_narration.export(temp_narration, format="mp3")

    ffmpeg_command = [
        'ffmpeg',
        '-y',
        '-i', input_video,
        '-i', temp_narration,
        '-map', '0:v',   # Map video from the first input
        '-map', '1:a',   # Map audio from the second input
        '-c:v', 'copy',  # Copy video codec
        '-c:a', 'aac',   # AAC audio codec
        '-strict', 'experimental',
        os.path.join(output_dir, output_file)
    ]

    subprocess.run(ffmpeg_command, capture_output=True)

    os.remove(temp_narration)

def resize_image(image, width, height):
    # Calculate the aspect ratio of the original image
    aspect_ratio = image.shape[1] / image.shape[0]

    # Calculate the new dimensions to fit within the desired size while preserving aspect ratio
    if aspect_ratio > (width / height):
        new_width = width
        new_height = int(width / aspect_ratio)
    else:
        new_height = height
        new_width = int(height * aspect_ratio)

    # Resize the image to the new dimensions without distorting it
    return cv2.resize(image, (new_width, new_height))

def create(narrations, output_dir, output_filename, caption_settings: dict|None = None):
    if caption_settings is None:
        caption_settings = {}

    # Define the dimensions and frame rate of the video
    width, height = 1080, 1920  # Change as needed for your vertical video
    frame_rate = 30  # Adjust as needed

    fade_time = 1000

    # Create a VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can change the codec as needed
    temp_video = os.path.join(output_dir, "temp_video.avi")  # Output video file name
    out = cv2.VideoWriter(temp_video, fourcc, frame_rate, (width, height))

    # List of image file paths to use in the video
    image_paths = os.listdir(os.path.join(output_dir, "images"))  # Replace with your image paths
    image_count = len(image_paths)

    # Load images and perform the transition effect
    for i in range(image_count):
        image1 = cv2.imread(os.path.join(output_dir, "images", f"image_{i+1}.webp"))

        if i+1 < image_count:
            image2 = cv2.imread(os.path.join(output_dir, "images", f"image_{i+2}.webp"))
        else:
            image2 = cv2.imread(os.path.join(output_dir, "images", f"image_1.webp"))

        image1 = resize_image(image1, width, height)
        image2 = resize_image(image2, width, height)

        narration = os.path.join(output_dir, "narrations", f"narration_{i+1}.mp3")
        duration = get_audio_duration(narration)

        if i > 0:
            duration -= fade_time

        if i == image_count-1:
            duration -= fade_time

        for _ in range(math.floor(duration/1000*30)):
            vertical_video_frame = np.zeros((height, width, 3), dtype=np.uint8)
            vertical_video_frame[:image1.shape[0], :] = image1

            out.write(vertical_video_frame)

        for alpha in np.linspace(0, 1, math.floor(fade_time/1000*30)):
            blended_image = cv2.addWeighted(image1, 1 - alpha, image2, alpha, 0)
            vertical_video_frame = np.zeros((height, width, 3), dtype=np.uint8)
            vertical_video_frame[:image1.shape[0], :] = blended_image

            out.write(vertical_video_frame)

    # Release the VideoWriter and close the window if any
    out.release()
    cv2.destroyAllWindows()

    # Add narration audio to video
    with_narration = "with_narration.mp4"
    add_narration_to_video(narrations, temp_video, output_dir, with_narration)

    # Add captions to video
    output_path = os.path.join(output_dir, output_filename)
    input_path = os.path.join(output_dir, with_narration)
    segments = create_segments(narrations, output_dir)

    captacity.add_captions(
        video_file=input_path,
        output_file=output_path,
        segments=segments,
        print_info=True,
        **caption_settings,
    )

    # Clean up temporary files
    os.remove(input_path)
    os.remove(temp_video)

def create_segments(narrations, output_dir):
    segments = []

    offset = 0
    for i, narration in enumerate(narrations):
        audio_file = os.path.join(output_dir, "narrations", f"narration_{i+1}.mp3")

        try:
            t_segments = captacity.transcriber.transcribe_locally(
                audio_file=audio_file,
                prompt=narration,
            )
        except ImportError:
            t_segments = captacity.transcriber.transcribe_with_api(
                audio_file=audio_file,
                prompt=narration,
            )

        o_segments = offset_segments(t_segments, offset)

        segments += o_segments
        offset += get_audio_duration(audio_file) / 1000

    return segments

def offset_segments(segments: list[dict], offset: float):
    for segment in segments:
        segment["start"] += offset
        segment["end"] += offset
        for word in segment["words"]:
            word["start"] += offset
            word["end"] += offset
    return segments
