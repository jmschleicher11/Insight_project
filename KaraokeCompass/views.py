from flask import render_template, request
from KaraokeCompass import app
from KaraokeCompass.Song_filter import filter_songs, song_listing


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
    
        # User's song information
        url = string + original_song['uri'].values[0] + "&theme=white"
        user_song = dict(Song=original_song['Song_x'].values[0], 
                         Artist=original_song['Artist'].values[0], 
                         Low_note=original_song['New_Low_Note'].values[0], 
                         High_note=original_song['New_High_Note'].values[0], 
                         uri=url)
        # Results song information
        for i in range(len(results)):
            url = string + results.iloc[i]['uri'] + "&theme=white"
            songs.append(dict(Song=results.iloc[i]['Song_x'], 
                              Artist=results.iloc[i]['Artist'], 
                              Low_note=results.iloc[i]['New_Low_Note'], 
                              High_note=results.iloc[i]['New_High_Note'],
                              uri=url))
    
        return render_template("output.html", songs=songs, user_song=user_song)

    else:
            
        # User's song information
        url = string + original_song['uri'].values[0] + "&theme=white"
        user_song = dict(Song=original_song['Song_x'].values[0], 
                     Artist=original_song['Artist'].values[0], 
                     Suggested_key='Original Key', 
                     Low_note=original_song['New_Low_Note'].values[0], 
                     High_note=original_song['New_High_Note'].values[0], 
                     uri=url)
        
        # Results song information
        for i in range(len(results)):
            url = string + results.iloc[i]['uri'] + "&theme=white"
            songs.append(dict(Song=results.iloc[i]['Song_x'], 
                              Artist=results.iloc[i]['Artist'], 
                              Suggested_key = results.iloc[i]['Suggested_key'], 
                              Low_note=results.iloc[i]['New_Low_Note'], 
                              High_note=results.iloc[i]['New_High_Note'], 
                              uri=url))
        
        return render_template("output_extra.html", songs=songs, 
                               user_song=user_song)
        
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/songs')
def songs():
    
    song_list = song_listing()
    
    songs=[]
    for i in range(len(song_list)):
        songs.append(dict(Song=song_list.iloc[i]['Song_x'],
                          Artist=song_list.iloc[i]['Artist']))
    
    return render_template("songs_list.html", songs=songs)