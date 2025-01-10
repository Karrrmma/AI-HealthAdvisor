import React, { useState } from 'react';

import './App.css';
import StudyBot from './Components/Chat';

function App() {
    return (
        <div className="App">
            <h1>Disease Checker</h1>
            <StudyBot />
        </div>
    );
}

export default App;
