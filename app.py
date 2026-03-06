from flask import Flask, request, render_template
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    transcript_text = ""
    error = ""
    lang_name = ""
    video_id = ""  # Initialize to avoid UnboundLocalError

    if request.method == 'POST':
        video_url = request.form.get('video_url')

        # Extract video ID from URL
        if "v=" in video_url:
            video_id = video_url.split("v=")[-1].split("&")[0]
        elif "youtu.be/" in video_url:
            video_id = video_url.split("youtu.be/")[-1].split("?")[0]
        else:
            error = "Invalid YouTube URL format."
            return render_template("tool.html", transcript=transcript_text, error=error, lang_name=lang_name, video_id=video_id)

      try:
    transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = "\n".join([line['text'] for line in transcript_data])
    lang_name = "Auto"
except TranscriptsDisabled:
    error = "Transcripts are disabled for this video."
except NoTranscriptFound:
    error = "No transcript found for this video."
except Exception as e:
    error = f"Error: {str(e)}"
            # First try manually created, then auto-generated
            try:
                transcript = transcript_list.find_manually_created_transcript(
                    [t.language_code for t in transcript_list])
            except NoTranscriptFound:
                transcript = transcript_list.find_generated_transcript(
                    [t.language_code for t in transcript_list])

            # Fetch transcript text
            transcript_data = transcript.fetch()
            transcript_text = "\n".join([line.text for line in transcript_data])
            lang_name = transcript.language  # Show actual transcript language name

        except TranscriptsDisabled:
            error = "Transcripts are disabled for this video."
        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template("tool.html", transcript=transcript_text, error=error, lang_name=lang_name, video_id=video_id)

