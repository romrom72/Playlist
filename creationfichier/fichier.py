def writeM3U(args, playlist):
    playlistFileName = args.nom_playlist +"."+ args.formatPlaylist
    playlistFile = open(playlistFileName, 'w')
    for champ_musique in playlist:
        playlistFile.write(champ_musique[8] + "\n")
    playlistFile.close()