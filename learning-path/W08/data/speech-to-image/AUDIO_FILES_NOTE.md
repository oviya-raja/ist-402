# Audio Files Note

## Required Audio Files

To complete the Speech-to-Image demonstrations, you need to create or record the following audio files:

### 1. `example1_sunset_mountains.wav` (or `.mp3`, `.m4a`)
- **Text to speak:** "A beautiful sunset over mountains"
- **Purpose:** Used for screenshot `07_transcription_displayed.png` and `09_generated_image_sunset.png`
- **How to create:**
  - Record yourself speaking the text
  - Use a text-to-speech tool
  - Use online TTS services (Google TTS, Amazon Polly, etc.)

### 2. `example3_futuristic_city.wav` (or `.mp3`, `.m4a`)
- **Text to speak:** "A futuristic cityscape at night with neon lights and flying vehicles"
- **Purpose:** Demonstrates abstract concept generation
- **How to create:** Same as above

## Quick Creation Methods

### Option 1: Text-to-Speech Online
- Use Google Translate TTS: https://translate.google.com
- Use online TTS tools
- Save the audio file

### Option 2: Record Audio
- Use your phone's voice recorder
- Use computer recording software (Audacity, QuickTime, etc.)
- Speak the text clearly

### Option 3: Python TTS (if available)
```python
# Example using gTTS (Google Text-to-Speech)
from gtts import gTTS
import os

text = "A beautiful sunset over mountains"
tts = gTTS(text=text, lang='en')
tts.save("example1_sunset_mountains.mp3")
```

## File Naming
- Keep the exact filenames as specified in README.md
- Supported formats: `.wav`, `.mp3`, `.m4a`, `.flac`
- Ensure audio is clear for best transcription accuracy
