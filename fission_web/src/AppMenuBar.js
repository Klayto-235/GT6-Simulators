import React from 'react';
import { MenuBar, Menu, MenuItemButton, MenuItemMenu, MenuItemSeparator } from './widgets/MenuBar';


function AppMenuBar() {
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

export default AppMenuBar;