# Note-Taking and Summarization Tool

## Overview
This project is designed to help students and learners create detailed summaries of their study materials. It enables users to generate concise plans for easier memorization and provides tests to check their understanding. All notes are stored on servers, allowing users to access them anywhere with an internet connection.

## Features
- **File Attachments**: Upload and attach audio, images, and text to notes.
- **Summarization**: Generate summaries based on uploaded materials (audio, text, images).
- **Text Editing**: Rich text formatting including bold, italics, strikethrough, underline, and bullet points.
- **Audio Processing**: Analyze audio materials using the Whisper speech-to-text model.
- **Test Generation**: Create and take tests based on your notes for self-assessment.
- **Cloud Storage**: All notes are stored in the cloud, ensuring access from anywhere.

## Technology
- **Backend**: Django
- **Audio Processing**: Whisper (for speech-to-text conversion)

## Installation and Setup
There are no specific library requirements. Simply install the project dependencies and run the Django server to get started.

1. Clone the repository:
   ```bash
   git clone https://github.com/MrApelsin4ik/ai_notes
   ```
2. Install dependencies for site server:
   ```bash
   pip install -r requirements.txt
   ```
3. Install dependencies for generating server:
   ```bash
   pip install -r requirements_gen_serv.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Put your server's ip to settings.py:
   Change ALLOWED_HOSTS = [] like this:
   ```bash
   ALLOWED_HOSTS = ['192.168.0.117']
   ```
6. Start the server:
   ```bash
   python manage.py runserver 0.0.0.0:80
   ```
7. Start the generator(Change the IP and port to your server):
   ```bash
   python stt3_2.py
   ```
## Usage
Once logged in or registered, the main page provides access to all the core features:
- Create new notes, attach files (audio, images, text), and edit the text with rich formatting.
- Use the summarization feature to generate concise versions of your notes.
- Upload audio files for automatic transcription via Whisper.

## Demo Video
Check out the [demo video](<https://drive.google.com/file/d/109bNl84fpLGkO24Ag5OJJWHqiuMFU4gL/view?usp=sharing)>) showcasing the prototype of the tool and its features.

## License
This project is currently freely available for use.

