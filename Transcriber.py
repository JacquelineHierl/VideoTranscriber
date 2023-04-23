import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
import logging
from logging.handlers import RotatingFileHandler


def transcript_mp4_to_text(video_path: str):
    r = sr.Recognizer()
    # specify the file path of the video
    # open the video file using an audio file reader
    video_audio = AudioSegment.from_file(video_path, "mp4")

    # set the chunk length in milliseconds
    chunk_length_ms = 100000
    # split the audio into chunks of the specified length
    chunks = make_chunks(video_audio, chunk_length_ms)
    # iterate through each chunk and transcribe the audio
    chunk_count = len(chunks)
    transcribed_text = ""

    for chunk in chunks:
        logging.info(f"Transkribiere Text, chunk index {chunks.index(chunk)} of {chunk_count - 1}")
        # export the audio chunk as a temporary WAV file
        chunk_filename = "temp.wav"
        chunk.export(chunk_filename, format="wav")

        # open the temporary WAV file using an audio file reader
        with sr.AudioFile(chunk_filename) as source:
            # read the audio data from the WAV file
            audio_data = r.record(source)

        # use the speech recognition object to recognize the text from the audio data
        chunk_text = r.recognize_google(audio_data, language="de-DE")

        # add the transcribed text from this chunk to the overall transcribed text
        transcribed_text += chunk_text + " "

    return transcribed_text


class Transcriber:
    def __init__(self, in_path: str, out_path: str):

        self.initLogger("", 3)
        output_text_file = os.path.join(out_path, "transcript_text" + "." + "txt")

        for file_path in in_path:
            file_name = os.path.basename(file_path)
            text_in_video = f"{file_name}"
            logging.info(f"{file_name} wird bearbeitet")
            text = transcript_mp4_to_text(file_path)
            text_in_video = f"{text_in_video}\n" \
                            f"{text}\n"
            with open(output_text_file, "a") as f:
                f.write("%s\n" % text_in_video)
                f.close()

    def initLogger(self, filename="", backups=0):
        logging.basicConfig(filename='MyLogger.log', filemode='w', encoding='utf-8', level=logging.DEBUG)
        logFormatter = logging.Formatter("%(asctime)s%(msecs)03d [%(threadName)s] [%(levelname)s]:  %(message)s",
                                         "%d.%m.%Y %H:%M:%S,")
        rootLogger = logging.getLogger()

        if filename != "":
            fileHandler = RotatingFileHandler(filename, mode='w', maxBytes=1048576, backupCount=backups)
            fileHandler.doRollover()
            fileHandler.setFormatter(logFormatter)
            rootLogger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)
