import streamlit as st
from ollama_utils import generate_response
from youtube_transcript_api import YouTubeTranscriptApi


prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """


## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        ytt_api = YouTubeTranscriptApi()
        transcript_text=ytt_api.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_ollama_content(transcript_text,prompt):

    model='gemma3'
    response=generate_response(prompt=prompt+transcript_text, model=model, temperature=0.2)
    return response

st.title("YouTube Transcript Summarizer")
youtube_link = st.text_input("Enter YouTube Video Link:")

## Testing the code
#youtube_link = "https://www.youtube.com/watch?v=EECUXqFrwbc"
#extract_transcript_details(youtube_link)


if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_ollama_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)




