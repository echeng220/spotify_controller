import React from "react";
import { 
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
    Redirect
} from "react-router-dom";

import JoinRoomPage from "./JoinRoomPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";

export default function HomePage() {

    return (
            <Router> 
                <Routes>
                    <Route path='/' element={<span>This is the home page</span>} />
                    <Route path='/join' element={<JoinRoomPage />} />
                    <Route path='/create' element={<CreateRoomPage />} />
                    <Route path='/room/:roomCode' element={<Room />} />
                </Routes>
            </Router>
    );
}