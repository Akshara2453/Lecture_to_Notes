import os
import ffmpeg

def extract_audio(video_path, audio_dir):
    """
    Extracts audio from the given video file and saves it as a .wav file using ffmpeg.

    Args:
        video_path (str): Path to the uploaded video file.
        audio_dir (str): Directory where extracted audio will be stored.

    Returns:
        str: Path to the saved audio file.
    """
    try:
        # Ensure output directory exists
        os.makedirs(audio_dir, exist_ok=True)

        # Extract filename without extension
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        audio_path = os.path.join(audio_dir, f"{base_name}.wav")

        # Run ffmpeg to extract audio
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, format='wav', acodec='pcm_s16le', ac=1, ar='16000')
            .overwrite_output()
            .run(quiet=True)
        )

        return audio_path

    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None
