import React from 'react';
import { GlobalHotKeys } from 'react-hotkeys';
import { MenuBar, Menu, MenuItemButton, MenuItemMenu, MenuItemSeparator } from './widgets/MenuBar';


class AppMenuBar extends React.Component {
	constructor(props) {
		super(props);

		this.state = {testChecked: true};

		this.onClickTest = this.onClickTest.bind(this);

		this.hotkeys = <GlobalHotKeys keyMap={{
			TEST: "ctrl+k"
		}} handlers={{
			TEST: this.onClickTest
		}}/>;
	}

	onClickTest(event) {
		if (event) event.preventDefault();
		this.setState(state => ({testChecked: !state.testChecked}));
	}

	render() {
		return (
			<>
				{this.hotkeys}
				<MenuBar className="appMenuBar">
					<Menu header="File">
						<MenuItemButton name="New"/>
						<MenuItemButton name="Open"/>
						<MenuItemButton name="Save"/>
						<MenuItemButton name="Save As"/>
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
						<MenuItemButton name="Test" checked={this.state.testChecked} onClick={this.onClickTest} hotkey="Ctrl + K"/>
						<MenuItemButton name="Aaaaaaaaaaaaaaaaaaaaaaaaaaaa"/>
						<MenuItemButton name="Aaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbba" hotkey="blaaa"/>
						<MenuItemMenu name="Aaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbabbbbbbbbb">
							<MenuItemButton name="Test" checked={this.state.testChecked} onClick={this.onClickTest} hotkey="Ctrl + K"/>
							<MenuItemButton name="Aaaaaaaaaaaaaaaaaaaaaaaaaaaa"/>
							<MenuItemButton name="Aaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbba" hotkey="blaaa"/>
							<MenuItemMenu name="Aaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbabbbbbbbbb">
								<MenuItemButton name="Aaaaaaaaaaaaaaaaaaaaaaaaaaaa"/>
								<MenuItemSeparator/>
								<MenuItemMenu name="Aaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbabbbbbbbbb">
									<MenuItemButton name="Aaaaaaaaaaaaaaaaaaaaaaaaaaaa"/>
								</MenuItemMenu>
							</MenuItemMenu>
							<MenuItemSeparator/>
							<MenuItemMenu name="Menu">
								<MenuItemButton name="ccc"/>
								<MenuItemSeparator/>
								<MenuItemMenu name="Menu">
									<MenuItemButton name="Aaaaaaaaaaaaaaaaaaaaaaaaaaaa"/>
									<MenuItemSeparator/>
									<MenuItemMenu name="Menu">
										<MenuItemMenu name="Aaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbabbbbbbbbb"/>
										<MenuItemButton name="Aaaaaaaaaaaaaaaaaaaaaaaaaaaa"/>
									</MenuItemMenu>
								</MenuItemMenu>
							</MenuItemMenu>
						</MenuItemMenu>
						<MenuItemSeparator/>
						<MenuItemMenu name="Menu">
							<MenuItemButton name="ccc"/>
							<MenuItemSeparator/>
							<MenuItemMenu name="Menu">
								<MenuItemButton name="Aaaaaaaaaaaaaaaaaaaaaaaaaaaa"/>
								<MenuItemSeparator/>
								<MenuItemMenu name="Menu">
									<MenuItemMenu name="Aaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbabbbbbbbbb"/>
									<MenuItemButton name="Aaaaaaaaaaaaaaaaaaaaaaaaaaaa"/>
								</MenuItemMenu>
							</MenuItemMenu>
						</MenuItemMenu>
					</Menu>
				</MenuBar>
			</>
		);
	}
}

export default AppMenuBar;