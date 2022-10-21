import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { childrenClassValidator, recursiveMap } from '../util';


const ButtonStyle = styled.button`
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

	&.hasName img {
		padding: 0 calc(1px + 0.5em);
	}

	&.shaped {
		border: ${props => props.theme.base_border};
		background: linear-gradient(${props => props.theme.accent_bg}, ${props => props.theme.base_bg});

		&:hover {
			background: ${props => props.theme.accent_bg};
		}

		&:active {
			background-color: ${props => props.theme.secondary_active};
		}
	}
`;

class Button extends React.Component {
	constructor(props) {
		super(props);

		this.onClick = this.onClick.bind(this);
	}

	onClick() { // This is used to discard the event parameter that is passed to button onClick
		if (this.props.onClick) this.props.onClick();
	}

	render() {
		return (
			<ButtonStyle onClick={this.onClick} style={this.props.style} tabIndex={-1}
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

Button.defaultProps = {
	checked: false
};

class ButtonGroup extends React.Component {
	render() {
		return (
			<>
				{recursiveMap(this.props.children, child => (
				(child.type == Button && (child.props?.group == this.props?.id)) ? React.cloneElement(child, {
					onClick: this.props.onClickButton.bind(null, child.props.index),
					checked: this.props.activeButton == child.props.index
				}) : child))}
			</>
		);
	}
}

ButtonGroup.propTypes = {
	children: PropTypes.node,
	id: PropTypes.number,
	onClickButton: PropTypes.func,
	activeButton: PropTypes.number
};

ButtonGroup.defaultProps = {
	onClickButton: () => {},
	activeButton: -1
};

const CheckboxButton = styled.button`
	border: none;
	background-color: ${props => props.theme.base_bg};
	padding: 0 0.2em 0 0;
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
			<CheckboxButton onClick={this.props.onClick} className={this.props.className} style={this.props.style} tabIndex={-1}>
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

Checkbox.defaultProps = {
	checked: false
};

class DropdownItem extends React.Component {
	render() {
		return (
			<button onClick={this.props.onClick} tabIndex={-1}>
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
		padding: 0;

		&:hover {
			background: ${props => props.theme.accent_bg};
		}

		&:active {
			background-color: ${props => props.theme.secondary_active};
		}
	}

	& > button {
		display: flex;
		width: 100%;
		align-items: center;
		border: ${props => props.theme.base_border};
		border-radius: 3px;
		background: linear-gradient(${props => props.theme.accent_bg}, ${props => props.theme.base_bg});
		margin: 0;

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

	&.disabled > button {
		background:${props => props.theme.base_bg};

		span:nth-child(2), img {
			visibility: hidden;
		}
	}
`;

class Dropdown extends React.Component {
	constructor(props) {
		super(props);

		this.ref = React.createRef();

		this.onClickOutside = this.onClickOutside.bind(this);
	}

	onClickOutside(event) {
		if (this.props.onClickOutside && !this.ref?.current.contains(event.target)) this.props.onClickOutside();
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
			<DropdownWrapper ref={this.ref} style={this.props.style} className={`${this.props.disabled ? "disabled" : ""} ${this.props.className ? this.props.className : ""}`}>
				<button onClick={this.props.onClickButton} tabIndex={-1}>
					<img draggable="false" src={this.props.children[this.props.activeItem].props.image}/>
					<span>{this.props.children[this.props.activeItem].props.name}</span>
					<span>▾</span>
				</button>
				{this.props.menuVisible &&
					<div style={{maxHeight: this.props?.maxDropdownHeight}}>
						{React.Children.map(this.props.children, child => (++index, React.cloneElement(child, {
							key: index,
							onClick: this.props.onClickItem.bind(null, index, child.props?.name)
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
	maxDropdownHeight: PropTypes.string,
	disabled: PropTypes.bool,
	activeItem: PropTypes.number,
	menuVisible: PropTypes.bool,
	onClickButton: PropTypes.func,
	onClickItem: PropTypes.func,
	onClickOutside: PropTypes.func
};

Dropdown.defaultProps = {
	disabled: false,
	activeItem: 0,
	menuVisible: false,
	onClickButton: () => {},
	onClickItem: () => {}
};

export { Button, ButtonGroup, Checkbox, Dropdown, DropdownItem };