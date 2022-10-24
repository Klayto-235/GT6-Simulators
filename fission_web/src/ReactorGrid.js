import React from 'react';
import { ScrollArea } from './widgets/ScrollArea';


class ReactorGrid extends React.Component {
	render() {
		return (
			<ScrollArea className="reactorGrid">
				<div style={{background: "red", width: "300px", height: "300px"}}>
					reactorGrid
				</div>
			</ScrollArea>
		);
	}
}

export default ReactorGrid;