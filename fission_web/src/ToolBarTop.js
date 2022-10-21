import React from 'react';
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
					Grid size: 4x4
					<Button name="Shrink to fit" className="shaped" style={{display: "block", padding: "0.5ex 1em"}}/>
				</ToolItemBlank>
				<ToolItemSeparator/>
				<ToolItemBlank>
					{this.buttons.slice(0, 4).map(key => <SmallButton image={assets.utilityImages[key]} key={key} className="shaped"/>)}
					<br/>
					{this.buttons.slice(4).map(key => <SmallButton image={assets.utilityImages[key]} key={key} className="shaped"/>)}
				</ToolItemBlank>
				<ToolItemSpacer style={{flexGrow: 1}}/>
				<ToolItemBlank style={{textAlign: "left", lineHeight: "1.5em"}}>
					<Checkbox name="Autoexpand"/>
					<br/>
					<Checkbox name="Show HU/t"/>
				</ToolItemBlank>
				<ToolItemSeparator/>
				<ToolItemBlank style={{textAlign: "left", lineHeight: "1.5em"}}>
					<Checkbox name="Autorun"/>
					<br/>
					<Checkbox name="Penalty Stop"/>
				</ToolItemBlank>
				<Button image={assets.utilityImages["Play"]}/>
			</ToolBar>
		);
	}
}

export default ToolBarTop;