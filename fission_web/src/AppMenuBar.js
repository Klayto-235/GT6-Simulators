import React from 'react';
import { MenuBar, Menu, MenuItemButton, MenuItemMenu, MenuItemSeparator } from './widgets/MenuBar';


class AppMenuBar extends React.Component {
	constructor(props) {
		super(props);

		this.state = {testChecked: true};

		this.onClickTest = this.onClickTest.bind(this);
	}

	onClickTest() {
		this.setState(prevState => ({testChecked: !prevState.testChecked}));
	}

	render() {
		return (
			<MenuBar className="appMenuBar">
				<Menu header="File">
					<MenuItemButton name="New"/>
					<MenuItemButton name="Open"/>
					<MenuItemButton name="Save"/>
					<MenuItemButton name="Save As"/>
					<MenuItemSeparator/>
					<MenuItemButton name="Quit"/>
				</Menu>
				<Menu header="Edit">
					<MenuItemButton name="Undo"/>
					<MenuItemButton name="Redo"/>
					<MenuItemSeparator/>
					<MenuItemButton name="Options"/>
				</Menu>
				<Menu header="Tools">
					<MenuItemButton name="Material Cost"/>
				</Menu>
				<Menu header="Help">
					<MenuItemButton name="Readme"/>
					<MenuItemButton name="About"/>
				</Menu>
				<Menu header="Test">
					<MenuItemButton name="Test" checked={this.state.testChecked} onClick={this.onClickTest}/>
					<MenuItemButton name="Aaaaaaaaaaaaaaaaaaaaaaaaaaaa"/>
					<MenuItemButton name="Aaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbba"/>
					<MenuItemSeparator/>
					<MenuItemMenu name="Menu">
						<MenuItemButton name="ccc"/>
						<MenuItemSeparator/>
						<MenuItemMenu name="Menu">
							<MenuItemButton name="Aaaaaaaaaaaaaaaaaaaaaaaaaaaa"/>
							<MenuItemSeparator/>
							<MenuItemMenu name="Menu">
								
							</MenuItemMenu>
						</MenuItemMenu>
					</MenuItemMenu>
				</Menu>
			</MenuBar>
		);
	}
}

export default AppMenuBar;