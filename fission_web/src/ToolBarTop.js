import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { ToolBar, ToolItemSeparator, ToolItemBlank, ToolItemSpacer } from './widgets/ToolBar';
import { Checkbox, Button } from './widgets/input';
import assets from './assets.js';


const SmallButton = styled(Button)`
	& img {
		width: 25px;
	}
`;

class ToolBarTop extends React.Component {
	constructor(props) {
		super(props);

		this.buttons = ["AddColLeft", "AddColRight", "AddRowTop", "AddRowBot", "RemColLeft", "RemColRight", "RemRowTop", "RemRowBot"];
	}
	
	render() {
		return (
			<ToolBar className="toolBarTop">
				<ToolItemBlank style={{lineHeight: "1.5em"}}>
					Grid size: {this.props.gridSize.join("x")}
					<Button name="Shrink to fit" className="shaped" style={{display: "block", padding: "0.5ex 1em"}} onClick={this.props.onClickShrinkToFit}/>
				</ToolItemBlank>
				<ToolItemSeparator/>
				<ToolItemBlank>
					{this.buttons.slice(0, 4).map((key, index) => <SmallButton image={assets.utilityImages[key]} key={key} className="shaped"
					onClick={this.props.onClickGridResize.bind(null, index)}/>)}
					<br/>
					{this.buttons.slice(4).map((key, index) => <SmallButton image={assets.utilityImages[key]} key={key} className="shaped"
					onClick={this.props.onClickGridResize.bind(null, index + 4)}/>)}
				</ToolItemBlank>
				<ToolItemSpacer style={{flexGrow: 1}}/>
				<ToolItemBlank style={{textAlign: "left", lineHeight: "1.5em"}}>
					<Checkbox name="Autoexpand" checked={this.props.isCheckedAutoexpand} onClick={this.props.toggleAutoexpand}/>
					<br/>
					<Checkbox name="Show HU/t" checked={this.props.isCheckedShowHUpt} onClick={this.props.toggleShowHUpt}/>
				</ToolItemBlank>
				<ToolItemSeparator/>
				<ToolItemBlank style={{textAlign: "left", lineHeight: "1.5em"}}>
					<Checkbox name="Autorun" checked={this.props.isCheckedAutorun} onClick={this.props.toggleAutorun}/>
					<br/>
					<Checkbox name="Penalty Stop" checked={this.props.isCheckedPenaltyStop} onClick={this.props.togglePenaltyStop}/>
				</ToolItemBlank>
				<Button image={assets.utilityImages["Play"]} onClick={this.props.onClickRun}/>
			</ToolBar>
		);
	}
}

ToolBarTop.propTypes = {
	gridSize:				PropTypes.array,
	onClickShrinkToFit:		PropTypes.func,
	onClickGridResize:		PropTypes.func,
	onClickRun:				PropTypes.func,
	toggleAutoexpand:		PropTypes.func,
	toggleShowHUpt:			PropTypes.func,
	toggleAutorun:			PropTypes.func,
	togglePenaltyStop:		PropTypes.func,
	isCheckedAutoexpand:	PropTypes.bool,
	isCheckedShowHUpt:		PropTypes.bool,
	isCheckedAutorun:		PropTypes.bool,
	isCheckedPenaltyStop:	PropTypes.bool
};

ToolBarTop.defaultProps = {
	gridSize:				[0, 0],
	onClickShrinkToFit:		() => {},
	onClickGridResize:		() => {},
	onClickRun:				() => {},
	toggleAutoexpand:		() => {},
	toggleShowHUpt:			() => {},
	toggleAutorun:			() => {},
	togglePenaltyStop:		() => {},
	isCheckedAutoexpand:	false,
	isCheckedShowHUpt:		false,
	isCheckedAutorun:		false,
	isCheckedPenaltyStop:	false
};

export default ToolBarTop;