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
            'qfmt': '{{Front}}<br>{{Audio}}',  # Front of the card
            'afmt': '{{Front}}<br><hr id="answer">{{Back}}<br>{{Audio}}',  # Back of the card
        },
    ]
)

# Create a deck
deck = genanki.Deck(
    2059400110,
    'Greek for Tourists'
)

# Greek phrases to include in the deck (Feel free to add/remove phrases)
phrases = [
    {"English": "Hello", "Greek": "Γειά σας"},
    {"English": "Goodbye", "Greek": "Αντίο"},
    {"English": "Please", "Greek": "Παρακαλώ"},
    {"English": "Thank you", "Greek": "Ευχαριστώ"},
    {"English": "Yes", "Greek": "Ναί"},
    {"English": "No", "Greek": "Όχι"},
    {"English": "How much?", "Greek": "Πόσο κοστίζει;"},
    {"English": "Where is the bathroom?", "Greek": "Πού είναι η τουαλέτα;"},
    {"English": "Do you speak English?", "Greek": "Μιλάτε Αγγλικά;"},
    {"English": "I don’t understand", "Greek": "Δεν καταλαβαίνω"},
]

# Add notes to the deck
for phrase in phrases:
    front_text = phrase["English"]
    back_text = phrase["Greek"]
    audio_file = generate_audio_gtts(phrase["Greek"])  # Use gTTS to generate audio

    # Create a note and add it to the deck
    note = create_note(model, front_text, back_text, audio_file)
    deck.add_note(note)

# Save the deck to a .apkg file in the dist directory
apkg_file = os.path.join(output_dir, 'greek_for_tourists.apkg')
package = genanki.Package(deck)
package.media_files = [os.path.join(output_dir, f"{phrase['Greek'].replace(' ', '_')}.mp3") for phrase in phrases]
package.write_to_file(apkg_file)

print(f"Anki deck '{apkg_file}' created with audio successfully!")
