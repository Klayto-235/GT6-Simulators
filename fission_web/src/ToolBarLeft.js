import React from 'react';
import PropTypes from 'prop-types';
import { GlobalHotKeys } from 'react-hotkeys';
import { ToolBar, ToolItemSeparator, ToolItemBlank } from './widgets/ToolBar';
import { Dropdown, DropdownItem, Button, ButtonGroup } from './widgets/input.js';
import assets from './assets.js';


class ToolBarLeft extends React.Component {
	constructor(props) {
		super(props);

		this.rodDropdownItems = Object.keys(assets.rodImages).filter(key => !["Ref", "Abs", "Mod"].includes(key));
		this.coolantDropdownItems = Object.keys(assets.coolantImages);

		this.hotkeys = <GlobalHotKeys handlers={{
			Rod1:		this.onClickTool.bind(this, 0),
			Rod2:		this.onClickTool.bind(this, 1),
			Rod3:		this.onClickTool.bind(this, 2),
			Rod4:		this.onClickTool.bind(this, 3),
			Ref:		this.onClickTool.bind(this, 4),
			Abs:		this.onClickTool.bind(this, 5),
			Mod:		this.onClickTool.bind(this, 6),
			Coolant1:	this.onClickTool.bind(this, 8),
			Coolant2:	this.onClickTool.bind(this, 9),
			Coolant3:	this.onClickTool.bind(this, 10),
			Coolant4:	this.onClickTool.bind(this, 11),
			Shape:		this.onClickTool.bind(this, 12),
			Reset:		this.onClickTool.bind(this, 13),
			Erase:		this.onClickTool.bind(this, 14)
		}}/>;

		this.state = {
			isDropdownMenuVisible: false
		};

		this.onClickTool =				this.onClickTool.bind(this);
		this.onClickDropdownItem =		this.onClickDropdownItem.bind(this);
		this.onClickOutsideDropdown =	this.onClickOutsideDropdown.bind(this);
		this.onClickButtonDropdown =	this.onClickButtonDropdown.bind(this);
	}
	
	onClickTool(buttonIndex) {
		this.setState({isDropdownMenuVisible: false});
		this.props.onClickTool(buttonIndex);
	}

	onClickOutsideDropdown() {
		this.setState({isDropdownMenuVisible: false});
	}

	onClickButtonDropdown() {
		this.setState((state, props) => {
			const tool = props.activeTool;
			const dropdownActive = (tool >= 0 && tool < 4) || (tool >= 8 && tool < 12);
			return {
				isDropdownMenuVisible: dropdownActive ? !state.isDropdownMenuVisible : state.isDropdownMenuVisible
			};
		});
	}

	onClickDropdownItem(itemIndex, itemName) {
		this.setState({isDropdownMenuVisible: false});
		this.props.onClickDropdownItem(itemIndex, itemName);
	}

	render() {
		const tool = this.props.activeTool;
		return (
			<>
				{this.hotkeys}
				<ToolBar className="toolBarLeft" horizontal={false}>
					{(tool < 8 || tool >= 12) && (
					<Dropdown style={{width: "100%", marginBottom: "2px"}} onClickItem={this.onClickDropdownItem} onClickOutside={this.onClickOutsideDropdown}
					onClickButton={this.onClickButtonDropdown} menuVisible={this.state.isDropdownMenuVisible} maxDropdownHeight="calc((52px + 1em)*8 + 18px)"
					activeItem={tool >= 0 && tool < 4 ? this.rodDropdownItems.indexOf(this.props.buttons[tool]) : 0} disabled={tool < 0 || tool >= 4}>
						{this.rodDropdownItems.map(key => <DropdownItem name={key} image={assets.rodImages[key]} key={key}/>)}
					</Dropdown>)}
					{(tool >= 8 && tool < 12) && (
					<Dropdown style={{width: "100%", marginBottom: "2px"}} onClickItem={this.onClickDropdownItem} onClickOutside={this.onClickOutsideDropdown}
					onClickButton={this.onClickButtonDropdown} menuVisible={this.state.isDropdownMenuVisible} maxDropdownHeight="calc((52px + 1em)*8 + 18px)"
					activeItem={this.coolantDropdownItems.indexOf(this.props.buttons[tool])}>
						{this.coolantDropdownItems.map(key => <DropdownItem name={key} image={assets.coolantImages[key]} key={key}/>)}
					</Dropdown>)}
					<ToolItemSeparator/>
					<ToolItemBlank>
						<ButtonGroup onClickButton={this.onClickTool} activeButton={tool}>
							<ButtonGroup id={1} onClickButton={this.props.onClickModifier} activeButton={this.props.activeModifier}>
								<ToolBar inline={true} horizontal={false}>
									{this.props.buttons.slice(0, 4).map((rod, index) => <Button name={rod} image={assets.rodImages[rod]} key={rod} index={index}/>)}
									<ToolItemSeparator/>
									{this.props.buttons.slice(4, 7).map((rod, index) => <Button name={rod} image={assets.rodImages[rod]} key={rod} index={index + 4}/>)}
									<ToolItemSeparator/>
									<Button name={this.props.buttons[7]} image={assets.utilityImages[this.props.buttons[7]]} group={1} index={7}/>
								</ToolBar>
								<ToolBar inline={true} horizontal={false}>
									{this.props.buttons.slice(8, 12).map((coolant, index) => <Button name={coolant} image={assets.coolantImages[coolant]} key={coolant} index={index + 8}/>)}
									<ToolItemSeparator/>
									{this.props.buttons.slice(12, 15).map((utility, index) => <Button name={utility} image={assets.utilityImages[utility]} key={utility} index={index + 12}/>)}
									<ToolItemSeparator/>
									<Button name={this.props.buttons[15]} image={assets.utilityImages[this.props.buttons[15]]} group={1} index={15}/>
								</ToolBar>
							</ButtonGroup>
						</ButtonGroup>
					</ToolItemBlank>
				</ToolBar>
			</>
		);
	}
}

ToolBarLeft.propTypes = {
	buttons:				PropTypes.array,
	activeTool:				PropTypes.number,
	activeModifier:			PropTypes.number,
	onClickTool:			PropTypes.func,
	onClickModifier:		PropTypes.func,
	onClickDropdownItem:	PropTypes.func
};

ToolBarLeft.defaultProps = {
	buttons: 				[],
	activeTool:				-1,
	activeModifier:			-1,
	onClickTool:			() => {},
	onClickModifier:		() => {},
	onClickDropdownItem:	() => {}
};

export default ToolBarLeft;