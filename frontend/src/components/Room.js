import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

export default function Room() {
    const [votesToSkip, setVotesToSkip] = useState(0);
    const [guestCanPause, setGuestCanPause] = useState(false);
    const [isHost, setIsHost] = useState(false);

    const { roomCode } = useParams();

    useEffect(() => {
        fetch(`/api/get-room?code=${roomCode}`)
        .then((response) => response.json())
        .then((data) => {
            console.log(`data: ${JSON.stringify(data)}`);

            setVotesToSkip(data.votesToSkip);
            setGuestCanPause(data.guestCanPause);
            setIsHost(data.isHost);
        });
    }, [])


    return (
        <div> 
            <h3>{roomCode}</h3>
            <p>{votesToSkip}</p>
            <p>Guest Can Pause: {guestCanPause.toString()}</p>
            <p>Host: {isHost.toString()}</p>
        </div>
    )
}
