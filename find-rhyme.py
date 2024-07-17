import json
import ast
import speech_recognition as sr
import time
import string
import pronouncing
import re

def doTheyRhyme(word1, word2):
    word1 = word1.translate(str.maketrans('', '', string.punctuation))
    word2 = word2.translate(str.maketrans('', '', string.punctuation))

    # Get the pronunciations for both words
    pronunciations1 = pronouncing.phones_for_word(word1)
    pronunciations2 = pronouncing.phones_for_word(word2)
    
    # Check if we have pronunciations for both words
    if not pronunciations1 or not pronunciations2:
        return False
    
    # Get the rhyming part of the first pronunciation of each word
    rhyme_part1 = pronouncing.rhyming_part(pronunciations1[0])
    rhyme_part2 = pronouncing.rhyming_part(pronunciations2[0])
    
    # Compare the rhyming parts
    return rhyme_part1 == rhyme_part2

def FindRhymeInLyric(spoke_last_word):
    # Find rhyme
    youtube_video_list = op('youtube_video_list')
    for row in range(youtube_video_list.numRows):
        lyrics = youtube_video_list[row, 1]
        
        try:
            # First, try to parse it as a JSON string
            lyrics_data = json.loads(lyrics.val)
        except json.JSONDecodeError:
            # If that fails, try to evaluate it as a Python literal
            try:
                lyrics_data = ast.literal_eval(lyrics.val)
            except:
                print(f"Unable to parse lyrics data in row {row}")
                continue
        
        # # Print the first item in lyrics_data
        # if lyrics_data and len(lyrics_data) > 0:
        #     print("First item in lyrics data:")
        #     print(lyrics_data[0])
        #     break  # Exit the loop after printing the first item
        # else:
        #     print(f"No lyrics data found for row {row}")

        for lyric in lyrics_data:
            regex = re.compile('[^a-zA-Z\s]')
            lyric_text = regex.sub('', lyric['text'])

            words = lyric_text.split()
            lyric_last_word = words[-1]
            

            if (doTheyRhyme(spoke_last_word, lyric_last_word)):
                print(lyric_text)

                # Play Audio
                audiofilein = op("audiofilein1")
                audiofilein.par.file = youtube_video_list[row, 0].val + ".wav"
                #audiofilein.par.cuepoint = lyric["start"]
                #
                audiofilein.par.trimstart = lyric["start"]
                audiofilein.par.trimend = lyric["start"] + (lyric["duration"])

                # Start playback
                audiofilein.par.play = True
                audiofilein.par.cue.pulse()

                
                op("feedback1").par.reset.pulse()

                return
            
    print("No Match!")

def onValueChange(channel, sampleIndex, val, prev):
    if val != 1:
        return

    # Get word from wav
    r = sr.Recognizer()
    hellow=sr.AudioFile('Speech.0.wav')
    with hellow as source:
        audio = r.record(source)
    try:
        s = r.recognize_google(audio)
        print(s)
    except Exception as e:
        print("Exception: "+ str(e))

    FindRhymeInLyric(s.split()[-1])

    return

