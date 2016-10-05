from moviepy.editor import VideoFileClip

DEFAULT_AUDIOFILE_CODEC = 'pcm_s16le' # i.e. wav, 16-bit
DEFAULT_AUDIOFILE_BITRATE = '16k'

def extract_audio_file(src_video_path, dest_audio_path,
                  audio_codec=DEFAULT_AUDIOFILE_CODEC,
                  audio_bitrate=DEFAULT_AUDIOFILE_BITRATE):
    """
    Given a video file, extracts the audio into a separate file
    Returns: the path to the extracted audio file

    src_video_path (str): absolute path to source video file

    src_audio_path (str): absolute destination path for audio file

    audio_codec (str): e.g. 'pcm_s16le', the default is 16bit WAV

    audio_bitrate (str): e.g. '16k'
    """

    movie = VideoFileClip(src_video_path)
    audio = movie.audio
    audio.write_audiofile(dest_audio_path,
                codec=audio_codec,bitrate=audio_bitrate)
    return dest_audio_path

testFile = 'videos/20161001_Weekly_Address_HD.mp4'

extract_audio_file(testFile, testFile.strip('mp4') + 'wav')
