import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import { Collapse } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";


export default function CreateRoomPage(
    {
        defaultVotesToSkip = 2,
        defaultGuestCanPause = true,
        updateRoom = false,
        roomCode = null,
        updateCallback = () => {}
    }) {

    const [votesToSkip, setVotesToSkip] = useState(defaultVotesToSkip);
    const [guestCanPause, setGuestCanPause] = useState(defaultGuestCanPause);
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const navigate = useNavigate();
    
    function handleVotesChange(e) {
        setVotesToSkip(e.target.value);
    }

    function handleGuestCanPauseChange(e) {
        setGuestCanPause(e.target.value === 'true' ? true : false);
    }

    function handleRoomButtonPressed() {
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(
                {
                    votesToSkip: votesToSkip,
                    guestCanPause: guestCanPause
                }
            )
        };

        fetch('/api/create-room', requestOptions)
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                navigate(`/room/${data.code}`, {replace: true});
            });
    }

    function handleUpdateButtonPressed() {
        const requestOptions = {
            method: 'PATCH',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(
                {
                    votesToSkip: votesToSkip,
                    guestCanPause: guestCanPause,
                    code: roomCode
                }
            )
        };

        fetch('/api/update-room', requestOptions)
            .then((response) => {
                if (response.ok) {
                    setSuccessMessage("Room updated successfully!");
                } else {
                    setErrorMessage("Error updating room...");
                }
                updateCallback();
            });
    }

    function renderTitle() {
        const title = updateRoom ? "Update Room" : "Create A Room";
        return title;
    }

    function renderCreateButtons() {
        return (
            <Grid container spacing={1}>
            <Grid item xs={12} align="center">
                <Button color="primary" variant="contained" onClick={handleRoomButtonPressed}>
                    Create A Room
                </Button>
            </Grid>
            <Grid item xs={12} align="center">
                <Button color="secondary" variant="contained" to="/" component={Link}>
                    Back
                </Button>
            </Grid>
        </Grid>
        );
    }

    function renderUpdateButtons() {
        return (
            <Grid item xs={12} align="center">
                <Button color="primary" variant="contained" onClick={handleUpdateButtonPressed}>
                    Update Room
                </Button>
            </Grid>
        );
    }

    return (
        <div>
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Collapse in={successMessage != "" || errorMessage != ""}>
                        {successMessage != "" ? (
                            <Alert severity="success" onClose={() => {setSuccessMessage("")}}>{successMessage}</Alert>
                        ) : (
                            <Alert severity="error" onClose={() => {setErrorMessage("")}}>{errorMessage}</Alert>
                        )}
                    </Collapse>
                </Grid>
                <Grid item xs={12} align="center">
                    <Typography component="h4" variant="h4">
                        {renderTitle()}
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <FormControl component="fieldset">
                        <FormHelperText>
                            <div align='center'>
                                Guest Control of Playback State
                            </div>
                        </FormHelperText>
                        <RadioGroup 
                            row
                            defaultValue={defaultGuestCanPause.toString()}
                            onChange={handleGuestCanPauseChange}
                        >
                            <FormControlLabel 
                                value="true"
                                control={<Radio color="primary"/>}
                                label="Play/Pause"
                                labelPlacement="bottom"
                            />
                            <FormControlLabel 
                                value="false"
                                control={<Radio color="secondary"/>}
                                label="No Control"
                                labelPlacement="bottom"
                            />
                        </RadioGroup>
                    </FormControl>
                </Grid>
                <Grid item xs={12} align="center">
                    <FormControl>
                        <TextField 
                            required={true}
                            type="number"
                            onChange={handleVotesChange}
                            defaultValue={votesToSkip}
                            inputProps={
                                {
                                    min: 1,
                                    style: {textAlign: "center"}
                                }
                            }
                        />
                        <FormHelperText>
                            <div align="center">
                                Votes Required to Skip Song
                            </div>
                        </FormHelperText>
                    </FormControl>
                </Grid>
                {updateRoom ? renderUpdateButtons() : renderCreateButtons()}
            </Grid>
        </div>
    );
}
