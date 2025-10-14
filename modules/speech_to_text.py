import whisper
import os

def transcribe_audio(audio_path, model_size="base"):
    """
    Transcribes an audio file into text using the Whisper model.

    Args:
        audio_path (str): Path to the extracted audio file.
        model_size (str): Whisper model variant ('tiny', 'base', 'small', 'medium', 'large').

    Returns:
        str: Transcribed text.
    """
    try:
        # Load Whisper model
        model = whisper.load_model(model_size)

        # Transcribe audio
        result = model.transcribe(audio_path, fp16=False, language="en")

        # Extract the text
        transcript = result["text"].strip()

        return transcript

    except Exception as e:
        print(f"Error during transcription: {e}")
        return "Transcription failed. Please check the audio file."


if __name__ == "__main__":
    # Example test
    test_audio = "data/audio/sample.wav"
    if os.path.exists(test_audio):
        print(transcribe_audio(test_audio))
    else:
        print("Test audio not found.")
