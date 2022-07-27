def query(query_text):

    results = [
        {
            "id": str(x),
            "fileName": f"./static/data/speech_samples/sample-00000{x}.mp3",
            "start_proportion": x / 6,
            "podcast_title": f"Podcast title, episode {x}",
            "podcast_url": f"https://www.podcast{x}.com",  # keep the http(s)!
            "podcast_info": f"This is info to print about the chunk or podcast. Chunk {x} is really interesting...",
        }
        for x in range(5)
    ]

    return results
