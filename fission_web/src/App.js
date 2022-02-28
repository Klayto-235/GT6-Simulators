import React from 'react';
import MenuBar from './MenuBar';
import GridEditor from './GridEditor';
import InfoPanel from './InfoPanel';


function App() {
	return (
		<>
			<MenuBar/>
			<div className="contentWrapper">
				<GridEditor/>
				<InfoPanel/>
			</div>
		</>
	);
}

export default App;