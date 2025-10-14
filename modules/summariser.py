import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest

def summarise_text(transcript, ratio=0.2):
    """
    Summarises the given transcript using spaCy and a TextRank-like method.

    Args:
        transcript (str): Full transcript text from Whisper.
        ratio (float): Fraction of sentences to keep in summary (default: 0.2).

    Returns:
        str: Summarised version of the transcript.
    """
    try:
        # Load English model
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(transcript.replace("\n", " ").strip())

        # Build frequency table for words
        word_frequencies = {}
        for word in doc:
            if word.text.lower() not in STOP_WORDS and word.is_alpha:
                word_frequencies[word.text.lower()] = word_frequencies.get(word.text.lower(), 0) + 1

        # Normalize frequencies
        max_freq = max(word_frequencies.values(), default=1)
        for word in word_frequencies:
            word_frequencies[word] /= max_freq

        # Score sentences
        sentence_scores = {}
        for sent in doc.sents:
            for word in sent:
                if word.text.lower() in word_frequencies:
                    sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word.text.lower()]

        # Pick top sentences
        select_length = max(1, int(len(list(doc.sents)) * ratio))
        summary_sentences = nlargest(select_length, sentence_scores, key=sentence_scores.get)

        # Join sentences
        summary = " ".join([sent.text for sent in summary_sentences])
        return summary

    except Exception as e:
        print(f"Error during summarisation: {e}")
        # fallback for very short text
        return transcript[:500]

# --------------------------
# Example usage
if __name__ == "__main__":
    test_text = (
        "Artificial intelligence is transforming education. "
        "It helps students by generating summaries, flashcards, and quizzes from lectures."
    )
    print(summarise_text(test_text))
