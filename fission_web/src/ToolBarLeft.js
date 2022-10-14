import React from 'react';
import { ToolBar, ToolItemButton, ToolItemSeparator, ToolBarButtonGroup, ToolItemBlank } from './widgets/ToolBar';
import { Dropdown, DropdownItem } from './widgets/input.js';
import image from 'data-url:../../assets/img/fill_tool.png';
import assets from './Assets.js';


function ToolBarLeft() {
	return (
		<ToolBar className="toolBarLeft" horizontal={false}>
			<Dropdown textWidth="70px">
				{Object.entries(assets.rodImages).map(kv => <DropdownItem name={kv[0]} image={kv[1]} key={kv[0]} />)}
			</Dropdown>
			<ToolItemSeparator/>
			<ToolItemBlank>
				<ToolBarButtonGroup>
					<ToolBarButtonGroup id="1">
						<ToolBar inline={true} horizontal={false}>
							<ToolItemButton name="Fill" image={image}/>
							<ToolItemButton name="Fill" image={image}/>
							<ToolItemButton name="Fill" image={image}/>
							<ToolItemButton name="Fill" image={image}/>
							<ToolItemSeparator/>
							<ToolItemButton name="Fill" image={image}/>
							<ToolItemButton name="Fill" image={image}/>
							<ToolItemButton name="Fill" image={image}/>
							<ToolItemSeparator/>
							<ToolItemButton name="Fill" image={image} group="1"/>
						</ToolBar>
						<ToolBar inline={true} horizontal={false}>
							<ToolItemButton name="Fill" image={image}/>
							<ToolItemButton name="Fill" image={image}/>
							<ToolItemButton name="Fill" image={image}/>
							<ToolItemButton name="Fill" image={image}/>
							<ToolItemSeparator/>
							<ToolItemButton name="Fill" image={image}/>
							<ToolItemButton name="Fill" image={image}/>
							<ToolItemButton name="Fill" image={image}/>
							<ToolItemSeparator/>
							<ToolItemButton name="Fill" image={image} group="1"/>
						</ToolBar>
					</ToolBarButtonGroup>
				</ToolBarButtonGroup>
			</ToolItemBlank>
		</ToolBar>
	);
}

export default ToolBarLeft;