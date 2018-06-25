#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def filter_songs(song_title, energy, decade, extra_keys):
    
    import pandas as pd
    
    direct = '/Users/Floreana/Documents/Jobs/Insight/data/'
    # direct = '/home/ubuntu/Insight_files/'    

    all_songs = pd.read_pickle(direct + 'full_range_database.pickle')
    karaoke_songs = pd.read_pickle(direct + 'karaoke_range_database.pickle')
    
    if any(all_songs.Song_x.isin([song_title.upper()])):
    
        song_info = all_songs[all_songs.Song_x.str.lower() == 
                              song_title.lower()]
        gender = song_info['Gender'].values[0]
        if gender == 'F':
            karaoke_songs = karaoke_songs.sort_values(by=['Gender'], 
                                                      ascending=True)
        else:
            karaoke_songs = karaoke_songs.sort_values(by=['Gender'], 
                                                      ascending=False)

    else:
        return 0, 1
    # Error code 1 = song isn't in database

    
    # Get song range information
    low_value = song_info.Low_Value.values[0]
    high_value = song_info.High_Value.values[0]
    
    keys = {-2: 'A#/Bb', -1: 'B', 0: 'C', 1: 'C#/Bb', 2: 'D', 3: 'D#/Eb', 
            4: 'E', 5: 'F', 6: 'F#/Gb', 7: 'G', 8: 'G#/Ab', 9: 'A', 
            10: 'A#/Bb', 11: 'B', 12: 'C', 13: 'C#/Db'}

    if extra_keys is None:
        # Find the songs within the range of the user's song
        songs_in_range = karaoke_songs.loc[(karaoke_songs.Low_Value >= 
                                            low_value) & 
                                           (karaoke_songs.High_Value <= 
                                            high_value)]
    else:
        songs_in_range = karaoke_songs.loc[(karaoke_songs.Low_Value >= 
                                            low_value) & 
                                           (karaoke_songs.High_Value <= 
                                            high_value)]
        songs_in_range.loc[:, 'Suggested_key'] = pd.Series('Original Key', 
                          index=songs_in_range.index)


        raise_keys = karaoke_songs.loc[(karaoke_songs.Low_Value + 2 >= 
                                            low_value) & 
                                           (karaoke_songs.High_Value + 2 <= 
                                            high_value)]
        raise_keys.loc[:, 'Suggested_key'] = pd.Series(
                raise_keys['key'] - 2).map(keys)
        
        lower_keys = karaoke_songs.loc[(karaoke_songs.Low_Value - 2 >= 
                                            low_value) & 
                                           (karaoke_songs.High_Value - 2 <= 
                                            high_value)]
        lower_keys.loc[:, 'Suggested_key'] = pd.Series(
                lower_keys['key'] - 2).map(keys)
        
        songs_in_range = songs_in_range.append(raise_keys)
        songs_in_range = songs_in_range.append(lower_keys)
        
        songs_in_range = songs_in_range.drop_duplicates(
                subset={'Artist', 'Song_x'}, keep='first')
    
    user_energy = energy.lower()
    user_decade = decade.lower()
    
    # Energy
    if user_energy == 'high':
        output = songs_in_range.loc[songs_in_range.energy > 0.67]
    elif user_energy == 'medium': 
        output = songs_in_range.loc[(songs_in_range.energy <= 0.67) &
                                    (songs_in_range.energy > 0.33)]
    elif user_energy == 'low':
        output = songs_in_range.loc[songs_in_range.energy <= 0.33]
    else:
        output = songs_in_range
        
    # Decade
    if user_decade == '1960s':
        output = output.loc[output.album_date.values < 1970]
    elif user_decade == '1970s':
        output = output.loc[(output.album_date.values >= 1970) & 
                                    (output.album_date.values < 1980)]
    elif user_decade == '1980s':
        output = output.loc[(output.album_date.values >= 1980) & 
                                    (output.album_date.values < 1990)]
    elif user_decade == '1990s':
        output = output.loc[(output.album_date.values >= 1990) & 
                                    (output.album_date.values < 2000)]
    elif user_decade == '2000s':
        output = output.loc[(output.album_date.values >= 2000) & 
                                    (output.album_date.values < 2010)]
    elif user_decade == '2010s':
        output = output.loc[output.album_date.values >= 2010]
    else:
        output = output

    # Removes original song if part of the list
    output = output[-output.Song_x.isin([song_title.upper()])]
    if len(output) == 0:
        return 0, 2
    # Error code 2: song doens't have any matches

    return song_info, output

original_song, results = filter_songs('Hey Jude', 'High', '1970s', '1')
#print(test)