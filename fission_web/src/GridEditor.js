import React from 'react';
import { GlobalHotKeys } from 'react-hotkeys';
import ToolBarLeft from './ToolBarLeft';
import ToolBarTop from './ToolBarTop';
import { ScrollArea } from './widgets/ScrollArea';
import { ReactorBlock } from './widgets/ReactorBlock';
import config from './config.js';
import historian from './historian.js';


class GridBlockProperties {
	constructor() {
		this.coolant		= "None";
		this.label			= "";
		this.showProgress	= [false, false, false, false];
		this.progress		= [0, 0, 0, 0];
		this.rods			= ["None", "None", "None", "None"];
		this.labels1		= ["", "", "", ""];
		this.labels2		= ["", "", "", ""];
	}

	clone() {
		let other = new GridBlockProperties();
		other.coolant = this.coolant;
		other.label = this.label;
		other.showProgress = this.showProgress;
		other.progress = this.progress;
		other.rods = this.rods;
		other.labels1 = this.labels1;
		other.labels2 = this.labels2;
		return other;
	}
}
GridBlockProperties.idCounter = 1;


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
			Run:				this.onClickRun.bind(this),
			Undo:				historian.undo.bind(historian),
			Redo:				historian.redo.bind(historian)
		}} keyMap={{
			Undo: "ctrl+z",
			Redo: "ctrl+y"
		}}/>;

		this.state = {
			toolBarLeftButtons:		config.rods.concat("Ref", "Abs", "Mod", config.coolants, "Reset", "Fill", "Floodfill"),
			activeTool:				-1,
			activeModifier:			-1,
			gridBounds:				[0, 0, 1, 1],
			grid:					Array(Array(new GridBlockProperties())),
			scrollAreaOffset:		[0, 0],
			selectedSlot:			[0, 0, -1],
			isCheckedAutoexpand:	config.autoExpand,
			isCheckedShowHUpt:		config.showHUpt,
			isCheckedAutorun:		config.autoRun,
			isCheckedPenaltyStop:	config.penaltyStop
		};

		this.scrollAreaRef = React.createRef();

		this.onClickTool =						this.onClickTool.bind(this);
		this.onClickModifier =					this.onClickModifier.bind(this);
		this.onClickToolBarLeftDropdownItem =	this.onClickToolBarLeftDropdownItem.bind(this);
		this.onClickShrinkToFit =				this.onClickShrinkToFit.bind(this);
		this.onClickGridResize =				this.onClickGridResize.bind(this);
		this.onClickRun =						this.onClickRun.bind(this);
		this.onClickSlot =						this.onClickSlot.bind(this);
		this.toggleAutoexpand =					this.toggleAutoexpand.bind(this);
		this.toggleShowHUpt =					this.toggleShowHUpt.bind(this);
		this.toggleAutorun =					this.toggleAutorun.bind(this);
		this.togglePenaltyStop =				this.togglePenaltyStop.bind(this);
	}

	onClickShrinkToFit() {

	}

	onClickGridResize(buttonIndex) {
		// React update batching *should not* cause problems for historian
		// (see https://stackoverflow.com/questions/48563650/does-react-keep-the-order-for-state-updates/48610973#48610973)
		historian.commitEvent(this.onClickGridResize.bind(this, (buttonIndex + 4) % 8), this.onClickGridResize.bind(this, buttonIndex));
		this.setState(function(state) {
			let gridBounds = [...state.gridBounds];
			let grid = state.grid.map(line => ([...line]));
			let scrollAreaOffset = state.scrollAreaOffset.slice();
			switch (buttonIndex) {
				case 0:
					gridBounds[0] -= 1;
					grid.forEach(line => line.unshift(new GridBlockProperties()));
					scrollAreaOffset[0] -= 130 * this.scrollAreaRef.current.props.scaleBase ** this.scrollAreaRef.current.state.contentScaleLevel;
					break;
				case 1:
					gridBounds[2] += 1;
					grid.forEach(line => line.push(new GridBlockProperties()));
					break;
				case 2:
					gridBounds[1] -= 1;
					grid.unshift(Array(gridBounds[2] - gridBounds[0]).fill(0).map(() => new GridBlockProperties()));
					scrollAreaOffset[1] -= 130 * this.scrollAreaRef.current.props.scaleBase ** this.scrollAreaRef.current.state.contentScaleLevel;
					break;
				case 3:
					gridBounds[3] += 1;
					grid.push(Array(gridBounds[2] - gridBounds[0]).fill(0).map(() => new GridBlockProperties()));
					break;
				case 4:
					if (gridBounds[2] - gridBounds[0] > 1) {
						gridBounds[0] += 1;
						grid.forEach(line => line.shift());
						scrollAreaOffset[0] += 130 * this.scrollAreaRef.current.props.scaleBase ** this.scrollAreaRef.current.state.contentScaleLevel;
					}
					else historian.dropEvents();
					break;
				case 5:
					if (gridBounds[2] - gridBounds[0] > 1) {
						gridBounds[2] -= 1;
						grid.forEach(line => line.pop());
					}
					else historian.dropEvents();
					break;
				case 6:
					if (gridBounds[3] - gridBounds[1] > 1) {
						gridBounds[1] += 1;
						grid.shift();
						scrollAreaOffset[1] += 130 * this.scrollAreaRef.current.props.scaleBase ** this.scrollAreaRef.current.state.contentScaleLevel;
					}
					else historian.dropEvents();
					break;
				case 7:
					if (gridBounds[3] - gridBounds[1] > 1) {
						gridBounds[3] -= 1;
						grid.pop();
					}
					else historian.dropEvents();
					break;
			}
			historian.registerEvents();
			return {gridBounds: gridBounds, grid: grid, scrollAreaOffset: scrollAreaOffset};
		});
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

	onClickSlot(row, col, slot) {
		this.setState(function(state) {
			let grid = state.grid.map(line => (line.slice()));
			let clone = grid[row][col].clone();
			if (state.activeModifier < 0) {
				null;
			}
			return {grid: grid};
		});
	}

	render() {
		const onClickSlot = this.onClickSlot;
		const selectedSlot = this.state.selectedSlot;
		const rowOffset = this.state.gridBounds[1];
		const colOffset = this.state.gridBounds[0];
		return (
			<>
				{this.hotkeys}
				<div className="gridEditor">
					<ToolBarLeft buttons={this.state.toolBarLeftButtons} activeTool={this.state.activeTool} activeModifier={this.state.activeModifier}
					onClickDropdownItem={this.onClickToolBarLeftDropdownItem} onClickTool={this.onClickTool} onClickModifier={this.onClickModifier}/>
					<ToolBarTop gridSize={[this.state.gridBounds[2] - this.state.gridBounds[0], this.state.gridBounds[3] - this.state.gridBounds[1]]}
					isCheckedAutoexpand={this.state.isCheckedAutoexpand} isCheckedShowHUpt={this.state.isCheckedShowHUpt}
					isCheckedAutorun={this.state.isCheckedAutorun} isCheckedPenaltyStop={this.state.isCheckedPenaltyStop}
					onClickShrinkToFit={this.onClickShrinkToFit} onClickGridResize={this.onClickGridResize}
					toggleAutoexpand={this.toggleAutoexpand} toggleShowHUpt={this.toggleShowHUpt}
					toggleAutorun={this.toggleAutorun} togglePenaltyStop={this.togglePenaltyStop}/>
					<ScrollArea className="reactorGrid" offset={this.state.scrollAreaOffset} ref={this.scrollAreaRef}>
						{this.state.grid.map(function(line, row) {
							return <React.Fragment key={row + rowOffset}>
								{line.map(function(block, col) {
									return <ReactorBlock key={col + colOffset} onClick={onClickSlot.bind(null, row, col)}
									checked={selectedSlot[0] == row && selectedSlot[1] == col ? selectedSlot[2] : -1}
									coolant={block.coolant} label={block.label} showProgress={block.showProgress} progress={block.progress}
									rods={block.rods} labels1={block.labels1} labels2={block.labels2}/>;})}
								<br/>
							</React.Fragment>;
						})}
					</ScrollArea>
				</div>
			</>
		);
	}
}

export default GridEditor;