import React, { Component } from "react";
import { render } from "react-dom";
import HomePage from "./HomePage";


export default class App extends Component {
    constructor(props) {
        super(props);

        // Modifying states will re-render the entire component
        // this.state = {}
    }

    render() {
        return (
            <div> 
                <HomePage />
            </div>
        );
    }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
