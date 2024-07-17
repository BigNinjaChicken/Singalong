from pytubefix import YouTube
from youtube_transcript_api import YouTubeTranscriptApi 
import os
from moviepy.editor import VideoFileClip

def onValueChange(channel, sampleIndex, val, prev):
    if val != 1:
        return

    youtube_video_list = op('youtube_video_list')

    for row in range(youtube_video_list.numRows):
        try:
            id_cell = youtube_video_list[row, 0]
            if id_cell is None or not hasattr(id_cell, 'val'):
                print(f"Invalid cell at row {row}, column 0")
                continue
            
            id = id_cell.val
            if not id:
                print(f"Empty video ID at row {row}")
                continue

            print(f"Processing video ID: {id}")
            
            # Download video
            yt = YouTube(f'https://youtu.be/{id}')
            video = yt.streams.filter(progressive=True, file_extension='mp4').first()
            default_filename = video.default_filename
            video.download()
            
            # Convert MP4 to WAV
            mp4_file = default_filename
            wav_file = f"{id}.wav"
            video_clip = VideoFileClip(mp4_file)
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(wav_file)
            
            # Close the clips
            audio_clip.close()
            video_clip.close()
            
            # Remove the original MP4 file
            os.remove(mp4_file)
            
            print(f"Video converted and saved as: {wav_file}")
            
        except Exception as e:
            print(f"Error processing row {row}: {str(e)}")

        # Get transcript
        try:
            srt = YouTubeTranscriptApi.get_transcript(id, languages=['en'])
            
            # Update transcript cell
            transcript_cell = youtube_video_list[row, 1]
            if transcript_cell is not None and hasattr(transcript_cell, 'val'):
                transcript_cell.val = srt
            else:
                print(f"Invalid transcript cell at row {row}, column 1")
        except Exception as e:
            print(f"Error getting transcript for video {id}: {str(e)}")

    return