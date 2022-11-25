import React from 'react';
import { Grid, Typography, Card, IconButton, LinearProgress } from "@material-ui/core"
import { PlayArrow, SkipNext, Pause } from "@mui/icons-material";



export default function MusicPlayer({
        imageUrl='../static/images/album_icon.png',
        title='Song Title',
        artist='Artist',
        isPlaying=false,
        time=0,
        duration=1
    }) {

    const songProgress = (time / duration) * 100;

    return(
        <Card>
            <Grid container alignItems='center'>
                <Grid item align='center' xs={4}>
                    <img src={imageUrl} height='100%' width='100%' />
                </Grid>
                <Grid item align='center' xs={8}>
                    <Typography component="h5" variant="h5">
                        {title}
                    </Typography>
                    <Typography color="textSecondary" variant="subtitle1">
                        {artist}
                    </Typography>
                    <div>
                        <IconButton>
                            {isPlaying ? <Pause /> : <PlayArrow />}
                        </IconButton>
                        <IconButton>
                            <SkipNext />
                        </IconButton>
                    </div>
                </Grid>
            </Grid>
            <LinearProgress variant="determinate" value={songProgress} />
        </Card>
    )
}