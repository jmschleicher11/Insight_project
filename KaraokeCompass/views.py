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

    results = filter_songs(song_title, energy, decade, extra_keys)
    if type(results) == str:
        return render_template("error.html")
        
    songs = []
    string = "https://open.spotify.com/embed?uri="
	
    if extra_keys is None:
    
        for i in range(len(results)):
            url = string + results.iloc[i]['uri'] + "&theme=white"
            songs.append(dict(Song=results.iloc[i]['Song_x'], 
                              Artist=results.iloc[i]['Artist'], uri=url))
    
        return render_template("output.html", songs=songs)

    else:
        
        for i in range(len(results)):
            url = string + results.iloc[i]['uri'] + "&theme=white"
            songs.append(dict(Song=results.iloc[i]['Song_x'], 
                              Artist=results.iloc[i]['Artist'], 
                              Suggested_key = results.iloc[i]['Suggested_key'], 
                              uri=url))
        
        return render_template("output_extra.html", songs=songs)
  #      return render_template("output_extra.html", songs=songs)
        
@app.route('/about')
def about():
    return render_template("about.html")