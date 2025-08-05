AUDIO FILES DIRECTORY
====================

This directory is for storing your MP3 and other audio files.

HOW TO ADD MP3 FILES:
1. Copy your MP3 files to this directory (/static/audio/)
2. Reference them in your HTML templates using Flask's url_for function:
   {{ url_for('static', filename='audio/your-file.mp3') }}

EXAMPLE FILES TO ADD:
- sample-bhajan.mp3
- om-namah-shivaya.mp3
- temple-bells.mp3
- bhajan1.mp3 (गणेश आरती)
- bhajan2.mp3 (शिव भजन)
- bhajan3.mp3 (हनुमान चालीसा)
- bhajan4.mp3 (कृष्ण भजन)
- maha-mantra.mp3

SUPPORTED FORMATS:
- MP3 (recommended - best browser support)
- OGG (open source alternative)
- WAV (uncompressed, larger files)
- AAC (good compression)

BEST PRACTICES:
- Keep file sizes reasonable for web (under 10MB per file)
- Use descriptive filenames
- Consider providing multiple formats for better browser compatibility
- Compress audio files for faster loading

To view examples of how to implement audio players, visit:
http://your-website.com/audio-examples