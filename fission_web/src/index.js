import React from 'react';
import ReactDOM from 'react-dom';
import { Normalize } from 'styled-normalize';
import { ThemeProvider } from 'styled-components';
import "./index.css";
import App from './App';


const theme = {
	base_fg: "black",
	base_bg: "#f0f0f0",
	base_border: "1px solid #d0d0d0",
	base_active: "#d0d0d0",
	accent_bg: "white",
	accent_border: "1px solid #808080",
	secondary_fg: "#808080",
	font_family: "sans-serif"
};

ReactDOM.render(
	<React.StrictMode>
		<Normalize/>
		<ThemeProvider theme={theme}>
			<App/>
		</ThemeProvider>
	</React.StrictMode>,
	document.getElementById("root"));