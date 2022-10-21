import React from 'react';
import { GlobalHotKeys } from 'react-hotkeys';
import { ToolBar, ToolItemSeparator, ToolItemBlank } from './widgets/ToolBar';
import { Dropdown, DropdownItem, Button, ButtonGroup } from './widgets/input.js';
import assets from './assets.js';
import config from './config.js';


class ToolBarLeft extends React.Component {
	constructor(props) {
		super(props);

		this.rodDropdownItems = Object.keys(assets.rodImages).filter(key => !["Ref", "Abs", "Mod"].includes(key));
		this.coolantDropdownItems = Object.keys(assets.coolantImages);

		this.hotkeys = <GlobalHotKeys handlers={{
			Rod1: this.onClickTool.bind(this, 0)
		}}/>;

		this.state = {
			buttons: config.rods.concat("Ref", "Abs", "Mod", "Fill", config.coolants, "Shape", "Reset", "Erase", "Floodfill"),
			activeTool: -1,
			activeModifier: -1,
			activeRodDropdownItem: 0,
			activeCoolantDropdownItem: 0,
			isDropdownMenuVisible: false
		};

		this.onClickTool = this.onClickTool.bind(this);
		this.onClickModifier = this.onClickModifier.bind(this);
		this.onClickRodDropdownItem = this.onClickRodDropdownItem.bind(this);
		this.onClickCoolantDropdownItem = this.onClickCoolantDropdownItem.bind(this);
		this.onClickOutsideDropdown = this.onClickOutsideDropdown.bind(this);
		this.onClickButtonDropdown = this.onClickButtonDropdown.bind(this);
	}
	
	onClickTool(buttonIndex) {
		this.setState(state => {
			const newActiveButton = buttonIndex == state.activeTool ? -1 : buttonIndex;
			return {
				activeTool: newActiveButton,
				activeRodDropdownItem: newActiveButton >= 0 && newActiveButton < 4 ? this.rodDropdownItems.indexOf(state.buttons[newActiveButton]) : state.activeRodDropdownItem,
				activeCoolantDropdownItem: newActiveButton >= 8 && newActiveButton < 12 ? this.coolantDropdownItems.indexOf(state.buttons[newActiveButton]) : state.activeCoolantDropdownItem,
				isDropdownMenuVisible: false
			};
		});
	}
	
	onClickModifier(buttonIndex) {
		this.setState(state => ({activeModifier: buttonIndex == state.activeModifier ? -1 : buttonIndex}));
	}

	onClickOutsideDropdown() {
		this.setState({isDropdownMenuVisible: false});
	}

	onClickButtonDropdown() {
		this.setState(state => {
			const tool = state.activeTool;
			const dropdownActive = (tool >= 0 && tool < 4) || (tool >= 8 && tool < 12);
			return {
				isDropdownMenuVisible: dropdownActive ? !state.isDropdownMenuVisible : state.isDropdownMenuVisible
			};
		});
	}

	onClickRodDropdownItem(itemIndex, itemName) {
		this.setState(state => {
			let buttons = [...state.buttons];
			buttons[state.activeTool] = itemName;
			return {
				buttons: buttons,
				activeRodDropdownItem: itemIndex,
				isDropdownMenuVisible: false
			};
		});
	}

	onClickCoolantDropdownItem(itemIndex, itemName) {
		this.setState(state => {
			let buttons = [...state.buttons];
			buttons[state.activeTool] = itemName;
			return {
				buttons: buttons,
				activeCoolantDropdownItem: itemIndex,
				isDropdownMenuVisible: false
			};
		});
	}

	render() {
		const tool = this.state.activeTool;
		return (
			<>
				{this.hotkeys}
				<ToolBar className="toolBarLeft" horizontal={false}>
					{(tool < 8 || tool >= 12) && (
					<Dropdown style={{width: "100%", marginBottom: "2px"}} onClickItem={this.onClickRodDropdownItem} onClickOutside={this.onClickOutsideDropdown}
					onClickButton={this.onClickButtonDropdown} menuVisible={this.state.isDropdownMenuVisible} maxDropdownHeight="calc((52px + 1em)*8 + 18px)"
					activeItem={this.state.activeRodDropdownItem} disabled={tool < 0 || tool >= 4}>
						{this.rodDropdownItems.map(key => <DropdownItem name={key} image={assets.rodImages[key]} key={key}/>)}
					</Dropdown>)}
					{(tool >= 8 && tool < 12) && (
					<Dropdown style={{width: "100%", marginBottom: "2px"}} onClickItem={this.onClickCoolantDropdownItem} onClickOutside={this.onClickOutsideDropdown}
					onClickButton={this.onClickButtonDropdown} menuVisible={this.state.isDropdownMenuVisible} maxDropdownHeight="calc((52px + 1em)*8 + 18px)"
					activeItem={this.state.activeCoolantDropdownItem}>
						{this.coolantDropdownItems.map(key => <DropdownItem name={key} image={assets.coolantImages[key]} key={key}/>)}
					</Dropdown>)}
					<ToolItemSeparator/>
					<ToolItemBlank>
						<ButtonGroup onClickButton={this.onClickTool} activeButton={tool}>
							<ButtonGroup id={1} onClickButton={this.onClickModifier} activeButton={this.state.activeModifier}>
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
			</>
		);
	}
}

export default ToolBarLeft;