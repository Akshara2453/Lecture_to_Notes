import re
import spacy

# Load spaCy English model (small, free)
nlp = spacy.load("en_core_web_sm")

def generate_flashcards(summary_text, max_cards=5):
    """
    Generates Q&A flashcards from the summarised text.

    Args:
        summary_text (str): Summarised text of the lecture.
        max_cards (int): Maximum number of flashcards to generate.

    Returns:
        list[dict]: List of flashcards with 'question' and 'answer' keys.
    """
    try:
        doc = nlp(summary_text)
        flashcards = []
        sentences = list(doc.sents)

        for sent in sentences[:max_cards]:
            sentence = sent.text.strip()

            # Use simple entity-based question generation
            entities = [(ent.text, ent.label_) for ent in sent.ents]
            if not entities:
                continue

            for ent_text, ent_label in entities:
                if ent_label in ["PERSON", "ORG"]:
                    question = f"Who is mentioned in the context: {sentence}?"
                    answer = ent_text
                elif ent_label in ["DATE", "TIME"]:
                    question = f"When did the event in this sentence occur: {sentence}?"
                    answer = ent_text
                elif ent_label in ["GPE", "LOC"]:
                    question = f"Where does this refer to: {sentence}?"
                    answer = ent_text
                elif ent_label in ["EVENT", "WORK_OF_ART"]:
                    question = f"What event or concept is described here: {sentence}?"
                    answer = ent_text
                else:
                    # General fallback: ask about the key idea
                    question = f"What is discussed in this sentence: {sentence}?"
                    answer = ent_text

                flashcards.append({
                    "question": question,
                    "answer": answer
                })

                # Limit total number of cards
                if len(flashcards) >= max_cards:
                    break

            if len(flashcards) >= max_cards:
                break

        return flashcards if flashcards else [{"question": "No flashcards could be generated.", "answer": ""}]

    except Exception as e:
        print(f"Error generating flashcards: {e}")
        return [{"question": "Error creating flashcards.", "answer": str(e)}]
