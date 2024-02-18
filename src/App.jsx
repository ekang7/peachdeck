import React from 'react';
import PptxReader from './components/PptxReader';
import './App.css'; 

function App() {
	return (
		<div className="App">
			<h1 className="app-logo">PeachDeck</h1>
			<img className = "logoimage" src="src/logo.jpg"></img>
			<PptxReader/>
		</div>
	);
}

export default App;
