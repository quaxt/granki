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
            'qfmt': '{{Front}}',  # Audio removed from the front of the card
            'afmt': '{{Front}}<br><hr id="answer">{{Back}}<br>{{Audio}}',  # Audio added to the back of the card
        },
    ]
)

# Create a deck
deck = genanki.Deck(
    2059400110,
    'Greek for Tourists'
)

# Read phrases from the phrases.txt file
phrases_file = 'phrases.txt'
phrases = read_phrases_from_file(phrases_file)

# Add notes to the deck
for phrase in phrases:
    front_text = phrase["English"]
    back_text = phrase["Greek"]
    audio_file = generate_audio_gtts(phrase["Greek"])  # Use gTTS to generate audio

    # Create a note and add it to the deck
    note = create_note(model, front_text, back_text, audio_file)
    deck.add_note(note)

# Save the deck to a .apkg file in the dist directory
apkg_file = os.path.join(output_dir, 'greek_1000_words.apkg')
package = genanki.Package(deck)
package.media_files = [os.path.join(output_dir, f"{phrase['Greek'].replace(' ', '_')}.mp3") for phrase in phrases]
package.write_to_file(apkg_file)

print(f"Anki deck '{apkg_file}' created with audio successfully!")
