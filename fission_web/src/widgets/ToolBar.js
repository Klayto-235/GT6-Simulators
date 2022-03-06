import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { children_class_validator } from './util';


class ToolItemSeparator extends React.Component {
	render() {
		return <span/>;
	}
}

class ToolItemButton extends React.Component {
	render() {
		return (
			<button className={(this.props.checked ? "checked" : "") + (this.props.name ? " hasName" : "")} onClick={this.props.onClick}>
				<img draggable="false" src={this.props.image}/>
				{this.props.name}
			</button>
		);
	}
}

ToolItemButton.propTypes = {
	name: PropTypes.string,
	image: PropTypes.string,
	onClick: PropTypes.func,
	checked: PropTypes.bool
};

class ToolBarButtonGroup extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			activeButton: -1
		};
	}

	onClick(buttonIndex) {
		this.setState(prevState => ({activeButton: buttonIndex == prevState.activeButton ? -1 : buttonIndex}));
	}

	render() {
		let index = -1;
		return (
			<>
				{React.Children.map(this.props.children, child => (++index, React.cloneElement(child, {
					key: index,
					onClick: this.onClick.bind(this, index),
					checked: this.state.activeButton == index
				})))}
			</>
		);
	}
}

ToolBarButtonGroup.propTypes = {
	children: children_class_validator([ToolItemSeparator, ToolItemButton])
};

const ToolBarWrapper = styled.div`
	display: flex;
	align-items: center;

	& > span {
		align-self: stretch;
		margin: 5px 2px;
		border-left: ${props => props.theme.secondary_border};
		border-right: ${props => props.theme.secondary_border};
		border-right-color: white;
	}

	& > button {
		font-size: 0.9em;
		padding: 0;
		margin: 0 1px;
		border: ${props => props.theme.base_border};
		border-color: ${props => props.theme.base_bg};
		border-radius: 3px;

		&:hover {
			background-color: ${props => props.theme.accent_bg};
			border: ${props => props.theme.base_border};
		}

		&.checked,
		&:active {
			background-color: ${props => props.theme.secondary_active};
			border: ${props => props.theme.base_border};
		}

		& img {
			display: block;
		}

		&.hasName {
			padding: 0 calc(1px + 0.5em);
		}
	}

	&.vertical {
		flex-direction: column;

		& > span {
			margin: 2px 5px;
			border: unset;
			border-top: ${props => props.theme.secondary_border};
			border-bottom: ${props => props.theme.secondary_border};
			border-bottom-color: white;
		}

		& > button {
			margin: 1px 0;
		}
	}
`;

class ToolBar extends React.Component {
	render() {
		let index = -1;
		return (
			<ToolBarWrapper className={(this.props.className + (this.props.horizontal ? "" : " vertical"))}>
				{React.Children.map(this.props.children, child => (++index, React.cloneElement(child, {
					key: index
				})))}
			</ToolBarWrapper>
		);
	}
}

ToolBar.propTypes = {
	className: PropTypes.string,
	horizontal: PropTypes.bool,
	children: children_class_validator([ToolItemSeparator, ToolItemButton, ToolBarButtonGroup])
};

ToolBar.defaultProps = {
	horizontal: true
};

export { ToolBar, ToolItemButton, ToolItemSeparator, ToolBarButtonGroup };