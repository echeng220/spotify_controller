import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Grid, Button, Typography } from '@material-ui/core';

export default function Room(props) {
    const [votesToSkip, setVotesToSkip] = useState(0);
    const [guestCanPause, setGuestCanPause] = useState(false);
    const [isHost, setIsHost] = useState(false);

    const navigate = useNavigate();

    const { roomCode } = useParams();

    useEffect(() => {
        fetch(`/api/get-room?code=${roomCode}`)
        .then((response) => {
            if (!response.ok) {
                console.log(`Room useEffect: ${props}`);
                navigate('/');
            } else {
                return response.json()
            }
        })
        .then((data) => {
            console.log(`data: ${JSON.stringify(data)}`);

            setVotesToSkip(data.votesToSkip);
            setGuestCanPause(data.guestCanPause);
            setIsHost(data.isHost);
        });
    }, [])

    function leaveButtonPressed() {
        console.log('leave button pressed');

        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"}
        }

        fetch('/api/leave-room', requestOptions)
            .then((response) => {
                console.log('leave-room api triggered');
                navigate('/');
            })
    }


    return (
        <Grid>
            <Grid item xs={12} align="center">
                <Typography variant="h4" component="h4">
                    Code: {roomCode}
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <Typography variant="h5" component="h5">
                    Host: {isHost.toString()}
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <Typography variant="h5" component="h5">
                    Votes: {votesToSkip}
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <Typography variant="h5" component="h5">
                    Can Pause: {guestCanPause.toString()}
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <Button variant="contained" color="secondary" onClick={leaveButtonPressed}>
                    Leave Room
                </Button>
            </Grid>
        </Grid>

    )
}

/*
<div>      
    <h3>{roomCode}</h3>
    <p>{votesToSkip}</p>
    <p>Guest Can Pause: {guestCanPause.toString()}</p>
    <p>Host: {isHost.toString()}</p>
</div>
*/