from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcript')
def transcript():
    url = request.args.get('url')
    video_id = url.split("v=")[1]
    
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([t['text'] for t in transcript])
    
    return jsonify({"transcript": text})

if __name__ == "__main__":
    app.run()
