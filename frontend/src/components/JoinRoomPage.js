import React, { useState } from "react";
import { TextField, Button, Grid, Typography } from "@material-ui/core";
import { Link, useNavigate } from "react-router-dom";


export default function JoinRoomPage() {
    const [roomCode, setroomCode] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const navigate = useNavigate();

    function handleTextFieldChange(e) {
        setroomCode(e.target.value);
    }

    function roomButtonPressed() {
        console.log(`roomButtonPressed: ${roomCode}`);
        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(
                {
                    code: roomCode
                }
            )
        };

        fetch('api/join-room', requestOptions)
            .then((response) => {
                if (response.ok) {
                    navigate(`/room/${roomCode}`);
                } else {
                    setErrorMessage(
                        {
                            error: "Room not found"
                        }
                    )
                }
            })
            .catch((error) => {
                console.log(error);
            });
    }

    return (
        <div> 
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Typography variant="h4" component="h4">
                        Join a Room
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <TextField
                        error={!!errorMessage}
                        label="Code"
                        placeholder="Enter a Room Code"
                        value={roomCode}
                        helperText={errorMessage.error}
                        variant="outlined"
                        onChange={handleTextFieldChange}
                    />
                </Grid>
                <Grid item xs={12} align="center">
                    <Button variant="contained" color="primary" onClick={roomButtonPressed}>
                        Enter Room
                    </Button>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button variant="contained" color="secondary" to="/" component={Link}>
                        Back
                    </Button>
                </Grid>
            </Grid>
        </div>
    );
}