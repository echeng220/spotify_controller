import React from 'react';
import { Grid, Typography, Card, IconButton, LinearProgress } from "@material-ui/core"
import { PlayArrow, SkipNext, Pause } from "@mui/icons-material";

export default function MusicPlayer({
        imageUrl='../static/images/album_icon.png',
        title='Song Title',
        artist='Artist',
        isPlaying=false,
        time=0,
        duration=1,
        votes=0,
        votesToSkip=2
    }) {

    const songProgress = (time / duration) * 100;

    function playSong() {
        const requestOptions = {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'}
        };

        fetch('/spotify/play', requestOptions);
    }
    
    function pauseSong() {
        const requestOptions = {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'}
        };

        fetch('/spotify/pause', requestOptions);
    }

    function skipSong() {
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        };

        fetch('/spotify/skip', requestOptions);
    }

    return(
        <Card>
            <Grid container alignItems='center'>
                <Grid item align='center' xs={4}>
                    <img src={ imageUrl } height='100%' width='100%' />
                </Grid>
                <Grid item align='center' xs={8}>
                    <Typography component="h5" variant="h5">
                        { title }
                    </Typography>
                    <Typography color="textSecondary" variant="subtitle1">
                        { artist }
                    </Typography>
                    <Typography color="textSecondary" variant="subtitle2">
                        Votes to Skip: { votes } /{" "} { votesToSkip }
                    </Typography>
                    <div>
                        <IconButton onClick={() => { isPlaying ? pauseSong() : playSong() }}>
                            { isPlaying ? <Pause /> : <PlayArrow /> }
                        </IconButton>
                        <IconButton onClick={() => skipSong()}>
                            <SkipNext />
                        </IconButton>
                    </div>
                </Grid>
            </Grid>
            <LinearProgress variant="determinate" value={ songProgress } />
        </Card>
    )
}