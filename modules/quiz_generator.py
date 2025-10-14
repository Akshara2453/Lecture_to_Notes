import re
import random
import spacy

# Load spaCy English model (small, free)
nlp = spacy.load("en_core_web_sm")

def generate_quiz(summary_text, max_questions=5):
    """
    Generates simple multiple-choice questions from the summarised text.

    Args:
        summary_text (str): Summarised lecture text.
        max_questions (int): Maximum number of questions to generate.

    Returns:
        list[dict]: List of MCQ questions with options and answer.
    """
    try:
        doc = nlp(summary_text)
        sentences = list(doc.sents)
        quiz = []

        for sent in sentences:
            sentence = sent.text.strip()
            if not sentence:
                continue

            # Extract nouns for questions
            nouns = [token.text for token in sent if token.pos_ in ["PROPN", "NOUN"]]
            if not nouns:
                continue

            # Pick one noun as answer
            answer = random.choice(nouns)
            question = sentence.replace(answer, "_____")

            # Generate options
            options = [answer]
            distractors = random.sample(nouns + ["data", "model", "AI", "system", "algorithm"], 3)
            options.extend(distractors)
            options = list(set(options))  # Remove duplicates
            random.shuffle(options)

            quiz.append({
                "question": question,
                "options": options[:4],
                "answer": answer
            })

            if len(quiz) >= max_questions:
                break

        return quiz if quiz else [{"question": "No quiz questions could be generated.", "options": [], "answer": ""}]

    except Exception as e:
        print(f"Error generating quiz: {e}")
        return [{"question": "Error creating quiz.", "options": [], "answer": str(e)}]
