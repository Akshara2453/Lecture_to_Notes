import streamlit as st
import os
from modules.audio_extraction import extract_audio  # now uses ffmpeg-python
from modules.speech_to_text import transcribe_audio
from modules.summariser import summarise_text
from modules.notes_generator import generate_notes
from modules.flashcard_generator import generate_flashcards
from modules.quiz_generator import generate_quiz
from modules.utils import save_text_file, load_json, save_json

# ----------------------------
# Streamlit Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Lecture Voice-to-Notes Generator",
    layout="wide"
)

# ----------------------------
# Directory Setup
# ----------------------------
BASE_DIR = "data"
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
TRANSCRIPT_DIR = os.path.join(BASE_DIR, "transcripts")
SUMMARY_DIR = os.path.join(BASE_DIR, "summaries")
FLASHCARD_DIR = os.path.join(BASE_DIR, "flashcards")
QUIZ_DIR = os.path.join(BASE_DIR, "quizzes")
DB_PATH = os.path.join(BASE_DIR, "db.json")

for folder in [UPLOAD_DIR, AUDIO_DIR, TRANSCRIPT_DIR, SUMMARY_DIR, FLASHCARD_DIR, QUIZ_DIR]:
    os.makedirs(folder, exist_ok=True)

# ----------------------------
# App Title
# ----------------------------
st.title("🎓 Lecture Voice-to-Notes Generator")
st.markdown("Upload a recorded lecture video to generate notes, flashcards, and quizzes automatically.")

# ----------------------------
# File Upload
# ----------------------------
uploaded_video = st.file_uploader("Upload your lecture video", type=["mp4", "mkv", "avi"])

if uploaded_video:
    video_path = os.path.join(UPLOAD_DIR, uploaded_video.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_video.read())

    st.success(f"Video uploaded: {uploaded_video.name}")

    # ----------------------------
    # Step 1: Extract Audio
    # ----------------------------
    with st.spinner("Extracting audio from video..."):
        audio_path = extract_audio(video_path, AUDIO_DIR)
    if audio_path:
        st.success("Audio extraction complete.")
    else:
        st.error("Audio extraction failed.")
        st.stop()

    # ----------------------------
    # Step 2: Speech to Text
    # ----------------------------
    with st.spinner("Converting speech to text using Whisper..."):
        transcript = transcribe_audio(audio_path)
    transcript_file_name = os.path.splitext(uploaded_video.name)[0] + "_transcript.txt"
    transcript_path = save_text_file(transcript, TRANSCRIPT_DIR, transcript_file_name)
    st.success("Transcription complete.")

    # ----------------------------
    # Step 3: Summarisation
    # ----------------------------
    with st.spinner("Summarising transcript..."):
        summary = summarise_text(transcript)
    summary_file_name = os.path.splitext(uploaded_video.name)[0] + "_summary.txt"
    summary_path = save_text_file(summary, SUMMARY_DIR, summary_file_name)
    st.success("Summary generated.")

    # ----------------------------
    # Step 4: Notes and Flashcards
    # ----------------------------
    with st.spinner("Generating structured notes and flashcards..."):
        notes = generate_notes(summary)
        flashcards = generate_flashcards(summary)
    st.success("Notes and flashcards created.")

    # ----------------------------
    # Step 5: Quiz Generation
    # ----------------------------
    with st.spinner("Creating quiz questions..."):
        quiz = generate_quiz(summary)
    st.success("Quiz ready.")

    # ----------------------------
    # Save all results to JSON
    # ----------------------------
    data_record = {
        "video": uploaded_video.name,
        "transcript_path": transcript_path,
        "summary_path": summary_path,
        "notes": notes,
        "flashcards": flashcards,
        "quiz": quiz
    }
    db = load_json(DB_PATH)
    db[uploaded_video.name] = data_record
    save_json(DB_PATH, db)

    # ----------------------------
    # Display Results
    # ----------------------------
    st.header("📝 Generated Content")

    tabs = st.tabs(["Transcript", "Summary", "Notes", "Flashcards", "Quiz"])

    with tabs[0]:
        st.text_area("Transcript", transcript, height=300)

    with tabs[1]:
        st.text_area("Summary", summary, height=300)

    with tabs[2]:
        st.markdown("### Study Notes")
        st.write(notes)

    with tabs[3]:
        st.markdown("### Flashcards (Q&A)")
        for card in flashcards:
            st.markdown(f"**Q:** {card['question']}")
            st.markdown(f"**A:** {card['answer']}")
            st.markdown("---")

    with tabs[4]:
        st.markdown("### Quiz Questions")
        for i, q in enumerate(quiz, start=1):
            st.markdown(f"**{i}. {q['question']}**")
            for opt in q['options']:
                st.markdown(f"- {opt}")
            st.markdown(f"**Answer:** {q['answer']}")
            st.markdown("---")

    # ----------------------------
    # Downloads
    # ----------------------------
    st.download_button("Download Summary", summary, file_name=summary_file_name)
    st.download_button("Download Notes", notes, file_name="notes.txt")

else:
    st.info("Please upload a recorded lecture video to begin.")
