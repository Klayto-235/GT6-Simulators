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
		this.progress		= [0, 0, 0, 0];
		this.rods			= ["None", "None", "None", "None"];
		this.labels1		= ["", "", "", ""];
		this.labels2		= ["", "", "", ""];
	}

	clone() {
		let other = new GridBlockProperties();
		other.coolant = this.coolant;
		other.label = this.label;
		other.progress = this.progress.slice();
		other.rods = this.rods.slice();
		other.labels1 = this.labels1.slice();
		other.labels2 = this.labels2.slice();
		return other;
	}

	setRod(slot, rod) {
		this.rods[slot] = rod;
	}

	setCoolant(coolant) {
		this.coolant = coolant;
	}

	resetContents() {
		for (let i = 0; i < 4; ++i) this.setRod(i, "None");
		this.setCoolant("None");
	}
}


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
			historyCommit:			0,
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
		this.setState(function(state) {
			let gridBounds = [...state.gridBounds];
			let grid = state.grid.map(line => ([...line]));
			let scrollAreaOffset = state.scrollAreaOffset.slice();
			const historyCommit = state.historyCommit + 1;
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
					break;
				case 5:
					if (gridBounds[2] - gridBounds[0] > 1) {
						gridBounds[2] -= 1;
						grid.forEach(line => line.pop());
					}
					break;
				case 6:
					if (gridBounds[3] - gridBounds[1] > 1) {
						gridBounds[1] += 1;
						grid.shift();
						scrollAreaOffset[1] += 130 * this.scrollAreaRef.current.props.scaleBase ** this.scrollAreaRef.current.state.contentScaleLevel;
					}
					break;
				case 7:
					if (gridBounds[3] - gridBounds[1] > 1) {
						gridBounds[3] -= 1;
						grid.pop();
					}
					break;
			}
			return {gridBounds: gridBounds, grid: grid, scrollAreaOffset: scrollAreaOffset, historyCommit: historyCommit};
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
			return {toolBarLeftButtons: buttons};
		});
	}

	onClickSlot(rowID, colID, slot) {
		this.applyTool(rowID, colID, slot, null);
	}

	applyTool(rowID, colID, slot, tool) {
		this.setState(function(state) {
			if (tool === null) {
				if (state.activeTool < 0) tool = {type: 0};
				else if (state.activeTool >= 0 && state.activeTool < 7) 
					tool = {type: 1, name: state.toolBarLeftButtons[state.activeTool], mod: state.activeModifier};
				else if (state.activeTool >= 7 && state.activeTool < 11) 
					tool = {type: 2, name: state.toolBarLeftButtons[state.activeTool], mod: state.activeModifier};
				else if (state.activeTool == 11) 
					tool = {type: 3, mod: state.activeModifier};
			}

			let selectedSlot = state.selectedSlot;
			let grid = state.grid;
			let historyCommit = state.historyCommit;
			if (tool.type == 0) {
				if (rowID == selectedSlot[0] && colID == selectedSlot[1] && slot == selectedSlot[2]) selectedSlot = [null, null, -1];
				else selectedSlot = [rowID, colID, slot];
			}
			else {
				historyCommit += 1;
				grid = grid.map(line => (line.slice()));
				const row = rowID - state.gridBounds[1];
				const col = colID - state.gridBounds[0];
				if (tool.mod < 0) {
					let clone = grid[row][col].clone();
					switch (tool.type) {
						case 1:
							clone.setRod(slot, tool.name);
							break;
						case 2:
							clone.setCoolant(tool.name);
							break;
						case 3:
							clone.resetContents();
							break;
					}
					grid[row][col] = clone;
				}
				else if (tool.mod == 12) { // Fill
	
				}
				else if (tool.mod == 13) { // Floodfill
	
				}
			}

			return {grid: grid, selectedSlot: selectedSlot, historyCommit: historyCommit};
		});
	}

	componentDidUpdate(prevProps, prevState) {
		if (prevState.historyCommit != this.state.historyCommit) {
			let undoState = {
				gridBounds: prevState.gridBounds,
				grid: prevState.grid,
				scrollAreaOffset: prevState.scrollAreaOffset
			};
			let redoState = {
				gridBounds: this.state.gridBounds,
				grid: this.state.grid,
				scrollAreaOffset: this.state.scrollAreaOffset
			};
			historian.commitEvent(this.setState.bind(this, function(state) {
				if (state.selectedSlot[0] < undoState.gridBounds[0] || state.selectedSlot[0] >= undoState.gridBounds[2] ||
					state.selectedSlot[1] < undoState.gridBounds[1] || state.selectedSlot[1] >= undoState.gridBounds[3])
					undoState.selectedSlot = [null, null, -1];
					return undoState;
			}), this.setState.bind(this, function(state) {
				if (state.selectedSlot[0] < redoState.gridBounds[0] || state.selectedSlot[0] >= redoState.gridBounds[2] ||
					state.selectedSlot[1] < redoState.gridBounds[1] || state.selectedSlot[1] >= redoState.gridBounds[3])
					redoState.selectedSlot = [null, null, -1];
					return redoState;
			}));
			historian.registerEvents();
		}
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
							const rowID = row + rowOffset;
							return <React.Fragment key={rowID}>
								{line.map(function(block, col) {
									const colID = col + colOffset;
									return <ReactorBlock key={colID} onClick={onClickSlot.bind(null, rowID, colID)}
									checked={selectedSlot[0] == rowID && selectedSlot[1] == colID ? selectedSlot[2] : -1}
									coolant={block.coolant} label={block.label} progress={block.progress}
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