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
			Coolant1:	this.onClickTool.bind(this, 7),
			Coolant2:	this.onClickTool.bind(this, 8),
			Coolant3:	this.onClickTool.bind(this, 9),
			Coolant4:	this.onClickTool.bind(this, 10),
			Reset:		this.onClickTool.bind(this, 11)
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
			const dropdownActive = (tool >= 0 && tool < 4) || (tool >= 7 && tool < 11);
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
					{(tool < 7 || tool >= 11) && (
					<Dropdown style={{width: "100%", marginBottom: "2px"}} onClickItem={this.onClickDropdownItem} onClickOutside={this.onClickOutsideDropdown}
					onClickButton={this.onClickButtonDropdown} menuVisible={this.state.isDropdownMenuVisible} maxDropdownHeight="calc((52px + 1em)*8 + 18px)"
					activeItem={(tool >= 0 && tool < 4) ? this.rodDropdownItems.indexOf(this.props.buttons[tool]) : 0} disabled={tool < 0 || tool >= 4}>
						{this.rodDropdownItems.map(key => <DropdownItem name={key} image={assets.rodImages[key]} key={key}/>)}
					</Dropdown>)}
					{(tool >= 7 && tool < 11) && (
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
									{this.props.buttons.slice(0, 4).map((rod, index) => <Button name={rod} image={assets.rodImages[rod]} key={index} index={index}/>)}
									<ToolItemSeparator/>
									{this.props.buttons.slice(4, 7).map((rod, index) => <Button name={rod} image={assets.rodImages[rod]} key={index} index={index + 4}/>)}
								</ToolBar>
								<ToolBar inline={true} horizontal={false}>
									{this.props.buttons.slice(7, 11).map((coolant, index) => <Button name={coolant} image={assets.coolantImages[coolant]} key={index} index={index + 7}/>)}
									<ToolItemSeparator/>
									<Button name={this.props.buttons[11]} image={assets.utilityImages[this.props.buttons[11]]} index={11}/>
									<Button name={this.props.buttons[12]} image={assets.utilityImages[this.props.buttons[12]]} group={1} index={12}/>
									<Button name={this.props.buttons[13]} image={assets.utilityImages[this.props.buttons[13]]} group={1} index={13}/>
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