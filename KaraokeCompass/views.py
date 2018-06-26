from flask import render_template, request
from KaraokeCompass import app
from KaraokeCompass.Song_filter import filter_songs


@app.route('/')
@app.route('/input')
def songs_input():
    return render_template("input.html")


@app.route('/output')
def songs_output():
    
    song_title = request.args.get('song_title')
    energy = request.args.get('energy')
    decade = request.args.get('decade')
    extra_keys = request.args.get('extra_keys')

    original_song, results = filter_songs(song_title, energy, decade, 
                                          extra_keys)

    if isinstance(results, int):
        if results == 1:
            return render_template("error.html")
        elif results == 2:
            return render_template("redo.html")

    string = "https://open.spotify.com/embed?uri="


    songs = []

    if extra_keys is None:        
    
        url = string + original_song['uri'].values[0] + "&theme=white"
        user_song = dict(Song=original_song['Song_x'].values[0], 
                         Artist=original_song['Artist'].values[0], uri=url)
        
        for i in range(len(results)):
            url = string + results.iloc[i]['uri'] + "&theme=white"
            songs.append(dict(Song=results.iloc[i]['Song_x'], 
                              Artist=results.iloc[i]['Artist'], uri=url))
    
        return render_template("output.html", songs=songs, user_song=user_song)

    else:
        
        url = string + original_song['uri'].values[0] + "&theme=white"
        user_song = dict(Song=original_song['Song_x'].values[0], 
                     Artist=original_song['Artist'].values[0], 
                     Suggested_key='Original Key', uri=url)
        
        for i in range(len(results)):
            url = string + results.iloc[i]['uri'] + "&theme=white"
            songs.append(dict(Song=results.iloc[i]['Song_x'], 
                              Artist=results.iloc[i]['Artist'], 
                              Suggested_key = results.iloc[i]['Suggested_key'], 
                              uri=url))
        
        return render_template("output_extra.html", songs=songs, 
                               user_song=user_song)
        
@app.route('/about')
def about():
    return render_template("about.html")