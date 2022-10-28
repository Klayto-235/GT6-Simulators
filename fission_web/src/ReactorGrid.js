import React from 'react';
import { ScrollArea } from './widgets/ScrollArea';
import { ReactorBlock } from './widgets/ReactorBlock';


class ReactorGrid extends React.Component {
	render() {
		return (
			<ScrollArea className="reactorGrid">
				<ReactorBlock/><ReactorBlock/><br/>
				<ReactorBlock/><ReactorBlock/>
			</ScrollArea>
		);
	}
}

export default ReactorGrid;