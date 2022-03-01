import React from 'react';
import ReactDOM from 'react-dom';
import { Normalize } from 'styled-normalize';
import { ThemeProvider } from 'styled-components';
import "./index.css";
import App from './App';


const theme = {
	fg: "black",
	bg: "#f0f0f0",
	border: "#d0d0d0",
	button_active: "#d0d0d0",
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