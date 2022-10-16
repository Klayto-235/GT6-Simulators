import React from 'react';
import { ToolBar, ToolItemSeparator, ToolItemBlank } from './widgets/ToolBar';
import image from 'data-url:../../assets/img/fill_tool.png';
import { Checkbox, Dropdown, DropdownItem, Button } from './widgets/input';


class ToolBarTop extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			checked: true
		};

		this.onCheckboxClicked = this.onCheckboxClicked.bind(this);
	}

	onCheckboxClicked() {
		this.setState(prevState => ({checked: !prevState.checked}));
	}
	
	render() {
		return (
			<ToolBar className="toolBarTop">
				<Button name="Fill" image={image}/>
				<Button name="Fill"/>
				<ToolItemSeparator/>
				<Button image={image}/>
				<ToolItemBlank>
					<Checkbox name="test" checked={this.state.checked} onClick={this.onCheckboxClicked}/>
					<span>
						<input type="checkbox"/>
						<label> Bleee</label>
					</span>
				</ToolItemBlank>
				<ToolItemBlank>
					<Dropdown textWidth="2em" maxHeight="300px">
						<DropdownItem image={image}/>
						<DropdownItem image={image} name="Fill"/>
						<DropdownItem image={image} name="Fill"/>
						<DropdownItem image={image} name="Test"/>
						<DropdownItem name="None"/>
					</Dropdown>
				</ToolItemBlank>
			</ToolBar>
		);
	}
}

export default ToolBarTop;