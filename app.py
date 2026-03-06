from flask import Flask, request, render_template
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    transcript_text = ""
    error = ""
    lang_name = ""
    video_id = ""

    if request.method == 'POST':
        video_url = request.form.get('video_url')

        # Check if URL is empty
        if not video_url:
            error = "Please enter a YouTube URL."
            return render_template("tool.html", transcript=transcript_text, error=error, lang_name=lang_name, video_id=video_id)

        # Extract video ID
        try:
            if "v=" in video_url:
                video_id = video_url.split("v=")[-1].split("&")[0]
            elif "youtu.be/" in video_url:
                video_id = video_url.split("youtu.be/")[-1].split("?")[0]
            else:
                raise ValueError("Invalid YouTube URL format.")
        except:
            error = "Invalid YouTube URL format."
            return render_template("tool.html", transcript=transcript_text, error=error, lang_name=lang_name, video_id=video_id)

        try:
            # Get transcripts
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            try:
                transcript = transcript_list.find_manually_created_transcript(
                    [t.language_code for t in transcript_list]
                )
            except NoTranscriptFound:
                transcript = transcript_list.find_generated_transcript(
                    [t.language_code for t in transcript_list]
                )

            transcript_data = transcript.fetch()

            transcript_text = "\n".join([line.text for line in transcript_data])
            lang_name = transcript.language

        except TranscriptsDisabled:
            error = "Transcripts are disabled for this video."
        except NoTranscriptFound:
            error = "No transcript found for this video."
        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template("tool.html", transcript=transcript_text, error=error, lang_name=lang_name, video_id=video_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)