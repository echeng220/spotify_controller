import React, { Component } from "react";
import { 
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
    Redirect
} from "react-router-dom";

import JoinRoomPage from "./JoinRoomPage";
import CreateRoomPage from "./CreateRoomPage";

export default class HomePage extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
                <Router> 
                    <Routes>
                        <Route path='/' element={<p>This is the home page</p>} />
                        <Route path='/join' element={<JoinRoomPage />} />
                        <Route path='/create' element={<CreateRoomPage />} />
                    </Routes>
                </Router>
        );
    }
}