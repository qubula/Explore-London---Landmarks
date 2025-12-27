# Voice Options for Alfie - London Cabbie Character

## Problem with OpenAI Standard Voices
The 6 default OpenAI voices (alloy, echo, fable, onyx, nova, shimmer) are too generic and American-sounding. They lack:
- Authentic London accent
- Middle-aged gravelly quality
- Character and personality
- Working-class warmth

## Better Solutions for Authentic Alfie Voice

### Option 1: ElevenLabs (RECOMMENDED)
**Best for:** Authentic character voices with emotion and accent control

**Advantages:**
- ✅ Extensive voice library with real accents
- ✅ British/London voices available (Adam, Charlie, etc.)
- ✅ Can clone voices or design custom voices
- ✅ High emotional range and natural delivery
- ✅ Voice Designer tool to create "middle-aged London cabbie"

**Pre-made Voices to Try:**
- **Adam** - Deep, middle-aged British male, authoritative
- **Charlie** - Casual Australian (can adjust to British)
- **George** - Warm British narrator
- **Bill** - Gruff, older male (good for cabbie)

**Custom Voice Design:**
1. Go to ElevenLabs Voice Lab
2. Adjust parameters:
   - Age: 45-55
   - Accent: British English (London)
   - Style: Conversational, warm
   - Tone: Gravelly, experienced
3. Generate sample and test
4. Use via API or Voice Library

**Pricing:**
- Starter: $5/month (30,000 characters = ~50-80 scripts)
- Creator: $11/month (100,000 characters = 150+ scripts)
- Pro: $99/month (500,000+ characters)

**API Integration:**
```python
from elevenlabs import generate, save
from elevenlabs import set_api_key

set_api_key("your-api-key")

audio = generate(
    text=script,
    voice="Adam",  # or custom voice ID
    model="eleven_monolingual_v1"
)

save(audio, "output.mp3")
```

---

### Option 2: Google Cloud Text-to-Speech
**Best for:** Authentic British accents, WaveNet quality

**Advantages:**
- ✅ Multiple British English variants (en-GB)
- ✅ WaveNet voices (very natural)
- ✅ Neural2 voices (balanced quality/cost)
- ✅ Specific accent control (British, Australian, etc.)

**Recommended Voices:**
- **en-GB-Neural2-B** - Male, British, deep voice
- **en-GB-Neural2-D** - Male, British, conversational
- **en-GB-Wavenet-B** - Male, British, premium quality

**Voice Customization:**
- Speaking rate: 0.9-1.0 (natural to slightly slower)
- Pitch: -2 to -4 (lower for middle-aged male)
- Volume gain: Adjust for cabbie recording quality

**Pricing:**
- WaveNet: $16 per 1M characters
- Neural2: $16 per 1M characters
- Standard: $4 per 1M characters
- **100 scripts × 370 chars = 37,000 chars → $0.59 (Neural2)**

**API Integration:**
```python
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

voice = texttospeech.VoiceSelectionParams(
    language_code="en-GB",
    name="en-GB-Neural2-B",
    ssml_gender=texttospeech.SsmlVoiceGender.MALE
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate=0.95,
    pitch=-3.0
)

response = client.synthesize_speech(
    input=synthesis_input,
    voice=voice,
    audio_config=audio_config
)
```

---

### Option 3: PlayHT
**Best for:** Ultra-realistic voices with emotion

**Advantages:**
- ✅ Hyper-realistic AI voices
- ✅ British accents available
- ✅ Emotion and style control
- ✅ Voice cloning possible

**Recommended Voices:**
- **Arthur** - British male, warm and conversational
- **Harry** - British male, mature
- **Ryan** - British male, energetic

**Pricing:**
- Creator: $39/month (12.5 hours of audio)
- Pro: $99/month (50 hours)

---

### Option 4: Voice Cloning (Most Authentic)
**Best for:** Creating the EXACT Alfie character

**Process:**
1. Record 5-10 minutes of someone doing Alfie's voice
2. Upload to ElevenLabs or PlayHT voice cloning
3. AI learns the voice characteristics
4. Generate scripts in that exact voice

**Requirements:**
- Clean audio recording
- Consistent accent and tone
- Various emotional ranges
- No background noise

**Where to Find Voice Actor:**
- Fiverr (£25-100 for voice recording)
- Voices.com
- Local acting groups
- Drama students

---

### Option 5: Microsoft Azure Neural Voices
**Best for:** Budget-friendly British voices

**Advantages:**
- ✅ Multiple British English voices
- ✅ Neural quality
- ✅ Affordable pricing

**Recommended Voices:**
- **en-GB-RyanNeural** - British male, conversational
- **en-GB-ThomasNeural** - British male, formal to casual

**Pricing:**
- Neural: $16 per 1M characters
- **100 scripts → $0.59**

---

## My Recommendation for Alfie

### Best Overall: **ElevenLabs with Adam voice OR custom designed voice**

**Why:**
1. **Adam voice** has the right depth and British quality
2. Can fine-tune age, accent, and character
3. Most natural-sounding for storytelling
4. Can add custom voice if needed later

**Implementation Plan:**
1. Sign up for ElevenLabs Starter ($5/month)
2. Test "Adam" voice with sample script
3. If not perfect, use Voice Design Lab to create custom cabbie
4. Generate all 50-100 scripts
5. Total cost: $5 subscription + no per-use charges (within limits)

### Budget Alternative: **Google Cloud Neural2-B**

**Why:**
1. Only $0.59 for 100 scripts
2. Authentic British accent
3. Can adjust pitch/speed for character
4. Pay-as-you-go (no subscription)

---

## Next Steps

1. **Choose your preferred service:**
   - ElevenLabs for best character voice
   - Google Cloud for budget British accent

2. **Test with sample script:**
   - Generate 2-3 samples
   - Compare quality and character
   - Verify accent authenticity

3. **Generate exhibition audio:**
   - Once voice is approved
   - Process all 50-100 scripts
   - Optimize for ESP32

**Which option interests you most?** I can help you:
- Set up ElevenLabs API and test Adam voice
- Try Google Cloud British voices
- Create custom voice parameters for either service
