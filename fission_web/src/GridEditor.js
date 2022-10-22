import React from 'react';
import { GlobalHotKeys } from 'react-hotkeys';
import ToolBarLeft from './ToolBarLeft';
import ToolBarTop from './ToolBarTop';
import ReactorGrid from './ReactorGrid';
import config from './config.js';


class GridEditor extends React.Component {
	constructor(props) {
		super(props);

		this.hotkeys = <GlobalHotKeys handlers={{
			Fill:				this.onClickModifier.bind(this, 7),
			Floodfill:			this.onClickModifier.bind(this, 15),
			ShrinkToFit:		this.onClickShrinkToFit.bind(this),
			IncrementLeft:		this.onClickGridResize.bind(this, 0),
			IncrementRight:		this.onClickGridResize.bind(this, 1),
			IncrementTop:		this.onClickGridResize.bind(this, 2),
			IncrementBottom:	this.onClickGridResize.bind(this, 3),
			DecrementLeft:		this.onClickGridResize.bind(this, 4),
			DecrementRight:		this.onClickGridResize.bind(this, 5),
			DecrementTop:		this.onClickGridResize.bind(this, 6),
			DecrementBottom:	this.onClickGridResize.bind(this, 7),
			Run:				this.onClickRun.bind(this)
		}}/>;

		this.state = {
			toolBarLeftButtons:		config.rods.concat("Ref", "Abs", "Mod", "Fill", config.coolants, "Shape", "Reset", "Erase", "Floodfill"),
			activeTool:				-1,
			activeModifier:			-1,
			gridSize:				[0, 0],
			isCheckedAutoexpand:	config.autoExpand,
			isCheckedShowHUpt:		config.showHUpt,
			isCheckedAutorun:		config.autoRun,
			isCheckedPenaltyStop:	config.penaltyStop
		};

		this.onClickTool =						this.onClickTool.bind(this);
		this.onClickModifier =					this.onClickModifier.bind(this);
		this.onClickToolBarLeftDropdownItem =	this.onClickToolBarLeftDropdownItem.bind(this);
		this.onClickShrinkToFit =				this.onClickShrinkToFit.bind(this);
		this.onClickGridResize =				this.onClickGridResize.bind(this);
		this.onClickRun =						this.onClickRun.bind(this);
		this.toggleAutoexpand =					this.toggleAutoexpand.bind(this);
		this.toggleShowHUpt =					this.toggleShowHUpt.bind(this);
		this.toggleAutorun =					this.toggleAutorun.bind(this);
		this.togglePenaltyStop =				this.togglePenaltyStop.bind(this);
	}

	onClickShrinkToFit() {

	}

	onClickGridResize(/*buttonIndex*/) {

	}

	onClickRun() {

	}

	toggleAutoexpand() {
		this.setState(state => ({isCheckedAutoexpand: !state.isCheckedAutoexpand}));
	}

	toggleShowHUpt() {
		this.setState(state => ({isCheckedShowHUpt: !state.isCheckedShowHUpt}));
	}

	toggleAutorun() {
		this.setState(state => ({isCheckedAutorun: !state.isCheckedAutorun}));
	}

	togglePenaltyStop() {
		this.setState(state => ({isCheckedPenaltyStop: !state.isCheckedPenaltyStop}));
	}

	onClickTool(buttonIndex) {
		this.setState(state => ({activeTool: buttonIndex == state.activeTool ? -1 : buttonIndex}));
	}

	onClickModifier(buttonIndex) {
		this.setState(state => ({activeModifier: buttonIndex == state.activeModifier ? -1 : buttonIndex}));
	}

	onClickToolBarLeftDropdownItem(itemIndex, itemName) {
		this.setState(state => {
			let buttons = [...state.toolBarLeftButtons];
			buttons[state.activeTool] = itemName;
			return {
				toolBarLeftButtons: buttons
			};
		});
	}

	render() {
		return (
			<>
				{this.hotkeys}
				<div className="gridEditor">
					<ToolBarLeft buttons={this.state.toolBarLeftButtons} activeTool={this.state.activeTool} activeModifier={this.state.activeModifier}
					onClickDropdownItem={this.onClickToolBarLeftDropdownItem} onClickTool={this.onClickTool} onClickModifier={this.onClickModifier}/>
					<ToolBarTop gridSize={this.state.gridSize} isCheckedAutoexpand={this.state.isCheckedAutoexpand} isCheckedShowHUpt={this.state.isCheckedShowHUpt}
					isCheckedAutorun={this.state.isCheckedAutorun} isCheckedPenaltyStop={this.state.isCheckedPenaltyStop} onClickShrinkToFit={this.onClickShrinkToFit}
					onClickGridResize={this.onClickGridResize} toggleAutoexpand={this.toggleAutoexpand} toggleShowHUpt={this.toggleShowHUpt}
					toggleAutorun={this.toggleAutorun} togglePenaltyStop={this.togglePenaltyStop}/>
					<ReactorGrid/>
				</div>
			</>
		);
	}
}

export default GridEditor;