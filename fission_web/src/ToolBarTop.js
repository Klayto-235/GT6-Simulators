import React from 'react';
import { ToolBar, ToolItemButton, ToolItemSeparator, ToolItemBlank } from './widgets/ToolBar';
import image from 'data-url:../../assets/img/fill_tool.png';
import { Checkbox, Dropdown, DropdownItem } from './widgets/input';


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
			<ToolItemButton name="Fill" image={image}/>
				<ToolItemButton name="Fill"/>
				<ToolItemSeparator/>
				<ToolItemButton image={image}/>
				<ToolItemBlank>
					<Checkbox name="test" checked={this.state.checked} onClick={this.onCheckboxClicked}/>
					<span>
						<input type="checkbox"/>
						<label> Bleee</label>
					</span>
				</ToolItemBlank>
				<ToolItemBlank>
					<Dropdown>
						<DropdownItem name="None"/>
						<DropdownItem image={image}/>
						<DropdownItem image={image} name="Fill"/>
						<DropdownItem image={image} name="Fill"/>
						<DropdownItem image={image} name="Test"/>
					</Dropdown>
				</ToolItemBlank>
			</ToolBar>
		);
	}
}

export default ToolBarTop;