from pytube import YouTube, Search

def download_audio(video_url, output_path='musica/'):
    try:
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path)
        return audio_stream.default_filename
    except Exception as e:
        print(f"Errore durante il download dell'audio: {str(e)}")
        return None

def get_youtube_info(url):
    """This function return: title, thumbnail, author and channel url"""
    youtube = YouTube(url)
    return youtube.title, youtube.thumbnail_url, youtube.author, youtube.channel_url  

def search_video_url(query):
    search_results = Search(query)
    return search_results.results[0].watch_url