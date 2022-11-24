import React, { useState, useEffect, useCallback } from "react";
import { 
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
    Navigate
} from "react-router-dom";
import { Grid, Button, ButtonGroup, Typography } from "@material-ui/core";

import JoinRoomPage from "./JoinRoomPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";

export default function HomePage(props) {
    const [roomCode, setRoomcode] = useState(null);

    useEffect(() => {
        fetch('/api/user-in-room')
            .then((response) => response.json())
            .then((data) => {
                console.log(`HomePage useEffect data: ${JSON.stringify(data)}`);
                setRoomcode(data.code);
            })
    }, []);

    function clearRoomCode() {
        console.log('clearRoomCode hit');
        setRoomcode(null);
    }

    function renderHomePage() {
        return (
            <Grid container spacing={3}>
                <Grid>
                    <Grid item xs={12} align="center">
                        <Typography variant="h3" component="h3">
                            House Party
                        </Typography>
                    </Grid>
                    <Grid item xs={12} align="center">
                        <ButtonGroup disableElevation variant="contained" color="primary">
                            <Button color="primary" to="/join" component={Link}>
                                Join a Room
                            </Button>
                            <Button color="secondary" to="/create" component={Link}>
                                Create a Room
                            </Button>
                        </ButtonGroup>
                    </Grid>
                </Grid>
                <Grid>
                    
                </Grid>
            </Grid>
        )
    }

    return (
            <Router> 
                <Routes>
                    <Route path='/' 
                        element={
                            roomCode ? (<Navigate to={`/room/${roomCode}`} />) : renderHomePage()
                        } 
                    />
                    <Route path='/join' element={<JoinRoomPage />} />
                    <Route path='/create' element={<CreateRoomPage />} />
                    <Route path='/room/:roomCode' element={<Room leaveRoomCallback={clearRoomCode}/>} />
                </Routes>
            </Router>
    );
}