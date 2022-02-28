import React from 'react';
import ToolBarLeft from './ToolBarLeft';
import ToolBarTop from './ToolBarTop';
import ReactorGrid from './ReactorGrid';


function GridEditor() {
	return (
		<div className="gridEditor">
			<ToolBarLeft/>
			<ToolBarTop/>
			<ReactorGrid/>
		</div>
	);
}

export default GridEditor;