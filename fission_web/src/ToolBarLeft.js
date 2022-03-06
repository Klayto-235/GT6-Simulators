import React from 'react';
import { ToolBar, ToolItemButton, ToolItemSeparator } from './widgets/ToolBar';
import image from 'data-url:../../assets/img/fill_tool.png';


function ToolBarLeft() {
	return (
		<ToolBar className="toolBarLeft" horizontal={false}>
			<ToolItemButton name="Fill" image={image}/>
			<ToolItemButton name="Fill"/>
			<ToolItemSeparator/>
			<ToolItemButton image={image}/>
		</ToolBar>
	);
}

export default ToolBarLeft;