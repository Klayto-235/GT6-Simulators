import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { childrenClassValidator, recursiveMap } from '../util';


const ButtonStyle = styled.button`
	font-size: 0.9rem;
	padding: 0;
	margin: 1px;
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
		padding: 0 calc(1px + 0.45rem);
	}
`;

class Button extends React.Component {
	render() {
		return (
			<ButtonStyle onClick={this.props.onClick} style={this.props.style}
			className={`${this.props.checked ? "checked" : ""} ${this.props.name ? "hasName" : ""} ${this.props.className ? this.props.className : ""}`}>
				<img draggable="false" src={this.props.image}/>
				{this.props.name}
			</ButtonStyle>
		);
	}
}

Button.propTypes = {
	name: PropTypes.string,
	image: PropTypes.string,
	onClick: PropTypes.func,
	checked: PropTypes.bool,
	group: PropTypes.number,
	index: PropTypes.number,
	className: PropTypes.string,
	style: PropTypes.object
};

class ButtonGroup extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			activeButton: -1
		};
	}

	onClick(buttonIndex) {
		this.setState(prevState => {
			const newActiveButton = buttonIndex == prevState.activeButton ? -1 : buttonIndex;
			if (this.props.onChange) this.props.onChange(newActiveButton);
			return {activeButton: newActiveButton};
		});
	}

	render() {
		return (
			<>
				{recursiveMap(this.props.children, child => (
				(child.type == Button && (child.props?.group == this.props?.id)) ? React.cloneElement(child, {
					onClick: this.onClick.bind(this, child.props.index),
					checked: this.state.activeButton == child.props.index
				}) : child))}
			</>
		);
	}
}

ButtonGroup.propTypes = {
	children: PropTypes.node,
	id: PropTypes.number,
	onChange: PropTypes.func
};

const CheckboxButton = styled.button`
	border: none;
	background-color: ${props => props.theme.base_bg};
	font-size: 0.9rem;
	padding: 0 0.2rem 0 0;
	white-space: nowrap;

	& span {
		display: inline-block;
		font-size: 0.9em;
		margin-right: 0.3em;
		padding-left: 0.1em;
		width: 0.9em;
		height: 1em;
		border-radius: 1px;
		border: ${props => props.theme.base_border};
		background-color: ${props => props.theme.accent_bg};
	}

	&:hover span {
		border: ${props => props.theme.accent_border};
	}

	& span.unchecked {
		color: ${props => props.theme.accent_bg};
	}
`;

class Checkbox extends React.Component {
	render() {
		return (
			<CheckboxButton onClick={this.props.onClick} className={this.props.className} style={this.props.style}>
				<span className={this.props.checked ? "" : "unchecked"}>✓</span>
				{this.props.name}
			</CheckboxButton>
		);
	}
}

Checkbox.propTypes = {
	name: PropTypes.string,
	checked: PropTypes.bool,
	onClick: PropTypes.func,
	className: PropTypes.string,
	style: PropTypes.object
};

class DropdownItem extends React.Component {
	render() {
		return (
			<button onClick={this.props.onClick}>
				<img draggable="false" src={this.props.image}/>
				{this.props.name}
			</button>
		);
	}
}

DropdownItem.propTypes = {
	image: PropTypes.string,
	name: PropTypes.string,
	onClick: PropTypes.func
};

const DropdownWrapper = styled.div`
	position: relative;

	& button {
		font-size: 0.9rem;
		padding: 0;

		&:hover {
			background: ${props => props.theme.accent_bg};
		}
	}

	& > button {
		display: flex;
		width: 100%;
		align-items: center;
		border: ${props => props.theme.base_border};
		border-radius: 3px;
		background: linear-gradient(${props => props.theme.accent_bg}, ${props => props.theme.base_bg});
		margin: 0 1px;

		& span:nth-child(2) {
			flex: 1;
			text-align: left;
		}

		& span:last-child {
			margin-left: 0.5em;
		}
	}

	& div {
		border: ${props => props.theme.base_border};
		position: absolute;
		z-index: 1;
		margin: 0 1px;
		overflow-y: auto;

		& button {
			width: 100%;
			border: none;
			text-align: left;

			&:hover {
				border: none;
			}

			& img {
				vertical-align: middle;
			}
		}
	}
`;

class Dropdown extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			isMenuVisible: false,
			activeOption: 0
		};
		this.ref = React.createRef();

		this.toggleMenu = this.toggleMenu.bind(this);
		this.onClickOutside = this.onClickOutside.bind(this);
	}

	toggleMenu() {
		this.setState(prevState => ({
			isMenuVisible: !prevState.isMenuVisible
		}));
	}

	onClickOption(optionIndex) {
		this.setState({
			isMenuVisible: false,
			activeOption: optionIndex
		});
	}

	onClickOutside(event) {
		if (!this.ref?.current.contains(event.target)) {
			this.setState({isMenuVisible: false});
        }
	}

	componentDidMount() {
		document.addEventListener('mousedown', this.onClickOutside);
	}

	componentWillUnmount() {
		document.removeEventListener('mousedown', this.onClickOutside);
	}

	render() {
		let index = -1;
		return (
			<DropdownWrapper ref={this.ref} style={this.props.style} className={this.props.className}>
				<button onClick={this.toggleMenu}>
					<img draggable="false" src={this.props.children[this.state.activeOption].props.image}/>
					<span>{this.props.children[this.state.activeOption].props.name}</span>
					<span>▾</span>
				</button>
				{this.state.isMenuVisible &&
					<div style={{maxHeight: this.props?.maxHeight}}>
						{React.Children.map(this.props.children, child => (++index, React.cloneElement(child, {
							key: index,
							onClick: this.onClickOption.bind(this, index)
						})))}
					</div>
				}
			</DropdownWrapper>
		);
	}
}

Dropdown.propTypes = {
	style: PropTypes.object,
	className: PropTypes.string,
	children: childrenClassValidator([DropdownItem], 1),
	maxHeight: PropTypes.string
};

export { Button, ButtonGroup, Checkbox, Dropdown, DropdownItem };