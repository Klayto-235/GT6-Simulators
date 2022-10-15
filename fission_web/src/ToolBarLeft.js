import React from 'react';
import { ToolBar, ToolItemButton, ToolItemSeparator, ToolBarButtonGroup, ToolItemBlank } from './widgets/ToolBar';
import { Dropdown, DropdownItem } from './widgets/input.js';
import assets from './assets.js';
import config from './config.js';


class ToolBarLeft extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			rods: config.rods,
			coolants: config.coolants
		};
	}

	render() {
		return (
			<ToolBar className="toolBarLeft" horizontal={false}>
				<Dropdown textWidth="70px">
					{Object.entries(assets.rodImages).map(kv => <DropdownItem name={kv[0]} image={kv[1]} key={kv[0]}/>)}
				</Dropdown>
				<ToolItemSeparator/>
				<ToolItemBlank>
					<ToolBarButtonGroup>
						<ToolBarButtonGroup id="1">
							<ToolBar inline={true} horizontal={false}>
								{this.state.rods.map(rod => <ToolItemButton name={rod} image={assets.rodImages[rod]} key={rod}/>)}
								<ToolItemSeparator/>
								<ToolItemButton name="Ref" image={assets.rodImages["Ref"]}/>
								<ToolItemButton name="Abs" image={assets.rodImages["Abs"]}/>
								<ToolItemButton name="Mod" image={assets.rodImages["Mod"]}/>
								<ToolItemSeparator/>
								<ToolItemButton name="Fill" image={assets.utilityImages["Fill"]} group="1"/>
							</ToolBar>
							<ToolBar inline={true} horizontal={false}>
								{this.state.coolants.map(coolant => <ToolItemButton name={coolant} image={assets.coolantImages[coolant]} key={coolant}/>)}
								<ToolItemSeparator/>
								<ToolItemButton name="Shape" image={assets.utilityImages["Shape"]}/>
								<ToolItemButton name="Reset" image={assets.utilityImages["Reset"]}/>
								<ToolItemButton name="Erase" image={assets.utilityImages["Erase"]}/>
								<ToolItemSeparator/>
								<ToolItemButton name="Floodfill" image={assets.utilityImages["Floodfill"]} group="1"/>
							</ToolBar>
						</ToolBarButtonGroup>
					</ToolBarButtonGroup>
				</ToolItemBlank>
			</ToolBar>
		);
	}
}

export default ToolBarLeft;