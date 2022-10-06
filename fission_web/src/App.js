import React from 'react';
import styled from 'styled-components';
import AppMenuBar from './AppMenuBar';
import GridEditor from './GridEditor';
import InfoPanel from './InfoPanel';


const AppWrapper = styled.div`
	background-color: ${props => props.theme.base_bg};
	color: ${props => props.theme.base_fg};
	font-family: ${props => props.theme.font_family};
	image-rendering: pixelated;
	overflow: auto;
`;

function App() {
	return (
		<AppWrapper className="appWrapper">
			<AppMenuBar/>
			<div className="contentWrapper">
				<GridEditor/>
				<InfoPanel/>
			</div>
		</AppWrapper>
	);
}

export default App;