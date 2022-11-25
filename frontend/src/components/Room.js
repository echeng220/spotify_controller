import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Grid, Button, Typography } from '@material-ui/core';
import CreateRoomPage from './CreateRoomPage';


export default function Room(props) {
    const [votesToSkip, setVotesToSkip] = useState(0);
    const [guestCanPause, setGuestCanPause] = useState(false);
    const [isHost, setIsHost] = useState(false);
    const [showSettings, setShowSettings] = useState(false);
    const [spotifyAuthenticated, setSpotifyAuthenticated] = useState(false);

    const navigate = useNavigate();

    const { roomCode } = useParams();

    function getRoomDetails() {
        console.log('getRoomDetails');
        return fetch(`/api/get-room?code=${roomCode}`)
            .then((response) => {
                if (!response.ok) {
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

                console.log(`isHost: ${isHost.toString()}`);
                console.log(`data isHost: ${data.isHost.toString()}`);

                if (data.isHost) {
                    authenticateSpotify();
                }
            });
    }
    
    useEffect(() => {
        console.log('useEffect');
        getRoomDetails();
        console.log(`useEffect isHost: ${isHost.toString()}`);
    }, [])

    function authenticateSpotify() {
        console.log('authenticateSpotify');

        fetch('/spotify/is-authenticated')
            .then((response) => response.json())
            .then((data) => {
                setSpotifyAuthenticated(data.status);

                if (!data.status) {
                    fetch('/spotify/get-auth-url')
                        .then((response) => response.json())
                        .then((data) => {
                            window.location.replace(data.url);
                        });
                }
            });
    }

    function leaveButtonPressed() {
        console.log('leave button pressed');

        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"}
        }

        fetch('/api/leave-room', requestOptions)
            .then((response) => {
                console.log('leave-room api triggered');
                props.leaveRoomCallback();
                navigate('/');
            })
    }

    function renderSettingsButton() {
        return (
            <Grid item xs={12} align="center">
                <Button variant="contained" color="primary" onClick={() => setShowSettings(true)}>
                    Settings
                </Button>
            </Grid>
        )
    }
    
    if (showSettings) {
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <CreateRoomPage 
                        updateRoom={true}
                        defaultVotesToSkip={votesToSkip}
                        defaultGuestCanPause={guestCanPause}
                        roomCode={roomCode}
                        updateCallback={getRoomDetails}
                    />
                </Grid>
                <Grid item xs={12} align="center">
                    <Button variant="contained" color="secondary" onClick={() => setShowSettings(false)}>
                        Close Settings
                    </Button>
                </Grid>
            </Grid>
        );
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
                    Guests Can Pause: {guestCanPause.toString()}
                </Typography>
            </Grid>
            {isHost ? renderSettingsButton() : null}
            <Grid item xs={12} align="center">
                <Button variant="contained" color="secondary" onClick={leaveButtonPressed}>
                    Leave Room
                </Button>
            </Grid>
        </Grid>

    )
}
