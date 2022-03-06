import React from 'react';
import { ToolBar, ToolItemButton, ToolItemSeparator } from './widgets/ToolBar';
import image from 'data-url:../../assets/img/fill_tool.png';


function ToolBarTop() {
	return (
		<ToolBar className="toolBarTop">
		<ToolItemButton name="Fill" image={image}/>
			<ToolItemButton name="Fill"/>
			<ToolItemSeparator/>
			<ToolItemButton image={image}/>
		</ToolBar>
	);
}

export default ToolBarTop;