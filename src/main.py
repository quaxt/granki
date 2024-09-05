from gtts import gTTS
import genanki
import os

# Create the dist directory if it doesn't exist
output_dir = "dist"
os.makedirs(output_dir, exist_ok=True)

# Function to create audio file using Google Text-to-Speech
def generate_audio_gtts(phrase, lang_code="el"):
    # Use gTTS to generate the speech
    tts = gTTS(text=phrase, lang=lang_code, slow=False)

    # Save the audio file in the dist directory
    audio_file = os.path.join(output_dir, f"{phrase}.mp3".replace(" ", "_"))
    tts.save(audio_file)
    return audio_file

# Function to create a note (flashcard) with the given front, back, and audio
def create_note(model, front, back, audio_file):
    audio_tag = f"[sound:{os.path.basename(audio_file)}]"  # Use only the filename for the audio tag
    note = genanki.Note(
        model=model,
        fields=[front, back, audio_tag],
    )
    return note

# Function to read phrases from phrases.txt
def read_phrases_from_file(file_path):
    phrases = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) >= 2:  # Ensure there are at least English and Greek phrases
                english = parts[0].strip()
                greek = parts[1].strip()
                # Transliteration (parts[2]) is ignored
                phrases.append({"English": english, "Greek": greek})
    return phrases

# Function to read most common words from most_common.txt
def read_most_common_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read and strip whitespace from each line, convert to lowercase for case-insensitive comparison
        return [line.strip().lower() for line in file]

# Function to sort phrases based on the most common words list
def sort_phrases(phrases, most_common_words):
    # Separate matched and unmatched phrases
    matched = []
    unmatched = []

    # Create a lookup for common words for fast comparison
    common_word_set = set(most_common_words)

    # Map to keep matched phrases according to their position in the most_common list
    common_phrases = {word: [] for word in most_common_words}

    # Populate matched and unmatched lists
    for phrase in phrases:
        english_lower = phrase["English"].lower()
        if english_lower in common_word_set:
            common_phrases[english_lower].append(phrase)
        else:
            unmatched.append(phrase)

    # Combine phrases: matched ones first (in the order they appear in most_common.txt), then unmatched
    for word in most_common_words:
        matched.extend(common_phrases[word])

    return matched + unmatched

# Create a model for the flashcards (this defines how the cards will look)
model = genanki.Model(
    1607392319,
    'Basic Greek with Audio',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
        {'name': 'Audio'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Front}}<br>{{Audio}}',
            'afmt': '{{Front}}<br><hr id="answer">{{Back}}',
        },
    ]
)

# Create a deck
deck = genanki.Deck(
    2059400110,
    'Common Greek words'
)

# Read phrases and most common words from the files
phrases_file = 'phrases.txt'
most_common_file = 'most_common.txt'

phrases = read_phrases_from_file(phrases_file)
most_common_words = read_most_common_words(most_common_file)

# Sort the phrases based on their occurrence in most_common.txt
sorted_phrases = sort_phrases(phrases, most_common_words)

# Add notes to the deck
for phrase in sorted_phrases:
    front_text = phrase["Greek"]
    back_text = phrase["English"]
    audio_file = generate_audio_gtts(phrase["Greek"])  # Use gTTS to generate audio

    # Create a note and add it to the deck
    note = create_note(model, front_text, back_text, audio_file)
    deck.add_note(note)

# Save the deck to a .apkg file in the dist directory
apkg_file = os.path.join(output_dir, 'common_greek_words.apkg')
package = genanki.Package(deck)
package.media_files = [os.path.join(output_dir, f"{phrase['Greek'].replace(' ', '_')}.mp3") for phrase in sorted_phrases]
package.write_to_file(apkg_file)

print(f"Anki deck '{apkg_file}' created with audio successfully!")
