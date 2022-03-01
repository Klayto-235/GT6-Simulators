import React from 'react';
import MenuBar from './widgets/MenuBar';


function AppMenuBar() {
	return (
		<MenuBar className="appMenuBar" menus={[
			{header: "File", items: []},
			{header: "Edit", items: []},
			{header: "Tools", items: []},
			{header: "Help", items: []}
		]}/>
	);
}

export default AppMenuBar;