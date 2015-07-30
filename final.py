#This code creates a Spotify playlist based off of user inputted poem/string
#Author: Jeff Li

import spotipy
import spotipy.util as util
import itertools
import pprint

# Login info
token = util.prompt_for_user_token('spotify_user_name',
                                   scope = 'user-library-read',
                                   client_id = 'insert_client_id',
                                   client_secret = 'insert_client_secret',
                                   redirect_uri='https://www.google.com'
)

spotify = spotipy.Spotify()
if token:
    # String text
    text = raw_input("Please input your string/poem! (must be longer than one word) :) = ")
    def break_down(text):
        "Breaking down line of text into all possible combinations of string input while maintaining order (excluding entire string)"
        combos = []
        words = text.split()
        ns = range(1, len(words))
        for n in ns:
            for idxs in itertools.combinations(ns, n):
                combos.append([' '.join(words[i:j]) for i, j in zip((0,) + idxs, idxs + (None,))])
        return combos
    total_poem = break_down(text.lower())

    flattened = []
    for sublist in total_poem:
        for val in sublist:
            if val not in flattened:
                flattened.append(val.lower().encode('utf-8'))

    phrase_storage = {}
    for word_combination in total_poem: # looking at each potential word combination within the poem - e.g. "I like" from "I like candy"
         for each_word in word_combination:
             search_results = spotify.search(q=each_word,limit=50,type='track') #Using Spotify API to search each potential word combination
             # pprint.pprint(search_results['tracks']['items'])
             # pprint.pprint(search_results)
             for i in list(search_results['tracks']['items']):
                 # You can comment out the two print lines below if you wish
                 print  i['name'].encode('utf-8') + " (Spotify song title)"
                 print each_word.encode('utf-8') + " (Search phrase)"
                 if i['name'].lower().encode('utf-8') in flattened:
                    phrase_storage[i['name'].lower()] = i['name'] + " by " + i['artists'][0]['name'] + " " +  i['album']['external_urls']['spotify'] #Looking for matches within flattened list - if there is a match, put it into phrase storage list to merge with other list

    matcher = filter(lambda x: all(y in phrase_storage for y in x), total_poem)
    poem_playlist = map(lambda x: [phrase_storage[y] for y in x], matcher)
    if poem_playlist != []:
        print "Below are all of the possible song combinations to your string: " + text
        pprint.pprint(poem_playlist)
    else:
        print "I couldn't find a match! This is likely the result of \n a) spelling error \n b) Spotify doesn't have a combination of song titles matching this fragment \n c) the only match for this string is an entire song title \n d) Your poem is only one word long \n Here is your string: " + text + " - please try again!"
else:
    print "Token/verification error"