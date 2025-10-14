import re

def generate_notes(summary_text):
    """
    Converts the summarised lecture text into structured study notes.

    Args:
        summary_text (str): The summarised text from the summariser.

    Returns:
        str: Well-formatted study notes.
    """
    try:
        # Clean text
        text = re.sub(r'\s+', ' ', summary_text.strip())

        # Split into sentences
        sentences = re.split(r'(?<=[.!?]) +', text)

        # Create bullet points
        notes = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            # Start each point with a capital letter and end with a full stop
            formatted = sentence[0].upper() + sentence[1:]
            notes.append(f"- {formatted}")

        # Combine into note format
        formatted_notes = "\n".join(notes)
        return formatted_notes

    except Exception as e:
        print(f"Error generating notes: {e}")
        return "Error creating study notes."
