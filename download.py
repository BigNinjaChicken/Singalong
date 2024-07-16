# me - this DAT
# 
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
# 
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.

from pytubefix import YouTube
from youtube_transcript_api import YouTubeTranscriptApi 
import os

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
            video = yt.streams.first()
            default_filename = video.default_filename
            video.download()
            
            # Rename the file
            new_filename = f"{id}.{default_filename.split('.')[-1]}"
            os.rename(default_filename, new_filename)
            print(f"Video renamed to: {new_filename}")
            
        except Exception as e:
            print(f"Error processing row {row}: {str(e)}")

            # Get transcript
            srt = YouTubeTranscriptApi.get_transcript(id, languages=['en'])
            
            # Update transcript cell
            transcript_cell = youtube_video_list[row, 1]
            if transcript_cell is not None and hasattr(transcript_cell, 'val'):
                transcript_cell.val = srt
            else:
                print(f"Invalid transcript cell at row {row}, column 1")

        
    
    return