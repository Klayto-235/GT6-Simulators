import React from 'react';
import { ToolBar, ToolItemSeparator, ToolItemBlank } from './widgets/ToolBar';
import { Dropdown, DropdownItem, Button, ButtonGroup } from './widgets/input.js';
import assets from './assets.js';
import config from './config.js';


class ToolBarLeft extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			buttons: config.rods.concat("Ref", "Abs", "Mod", "Fill", config.coolants, "Shape", "Reset", "Erase", "Floodfill"),
			activeTool: -1,
			activeModifier: -1
		};
	}

	onChangeTool(buttonIndex) {
		this.setState({activeTool: buttonIndex});
	}

	onChangeModifier(buttonIndex) {
		this.setState({activeModifier: buttonIndex});
	}

	render() {
		return (
			<ToolBar className="toolBarLeft" horizontal={false}>
				<Dropdown style={{width: "100%"}} maxHeight="calc((52px + 1em)*8 + 18px)">
					{Object.entries(assets.rodImages).map(kv => <DropdownItem name={kv[0]} image={kv[1]} key={kv[0]}/>)}
				</Dropdown>
				<ToolItemSeparator/>
				<ToolItemBlank>
					<ButtonGroup onChange={this.onChangeTool}>
						<ButtonGroup id={1} onChange={this.onChangeModifier}>
							<ToolBar inline={true} horizontal={false}>
								{this.state.buttons.slice(0, 4).map((rod, index) => <Button name={rod} image={assets.rodImages[rod]} key={rod} index={index}/>)}
								<ToolItemSeparator/>
								{this.state.buttons.slice(4, 7).map((rod, index) => <Button name={rod} image={assets.rodImages[rod]} key={rod} index={index + 4}/>)}
								<ToolItemSeparator/>
								<Button name={this.state.buttons[7]} image={assets.utilityImages[this.state.buttons[7]]} group={1} index={7}/>
							</ToolBar>
							<ToolBar inline={true} horizontal={false}>
								{this.state.buttons.slice(8, 12).map((coolant, index) => <Button name={coolant} image={assets.coolantImages[coolant]} key={coolant} index={index + 8}/>)}
								<ToolItemSeparator/>
								{this.state.buttons.slice(12, 15).map((utility, index) => <Button name={utility} image={assets.utilityImages[utility]} key={utility} index={index + 12}/>)}
								<ToolItemSeparator/>
								<Button name={this.state.buttons[15]} image={assets.utilityImages[this.state.buttons[15]]} group={1} index={15}/>
							</ToolBar>
						</ButtonGroup>
					</ButtonGroup>
				</ToolItemBlank>
			</ToolBar>
		);
	}
}

export default ToolBarLeft;