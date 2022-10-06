import React from 'react';
import PropTypes from 'prop-types';
import styled, { ThemeConsumer } from 'styled-components';
import { children_class_validator } from './util';


const CheckboxButton = styled.button`
	border: none;
	background-color: ${props => props.theme.base_bg};
	font-size: 0.9rem;
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
			<CheckboxButton onClick={this.props.onClick} className={this.props.className}>
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
	className: PropTypes.string
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

	& > button {
		width: 100%;
		border: ${props => props.theme.base_border};
		border-radius: 3px;
		background: linear-gradient(${props => props.theme.accent_bg}, ${props => props.theme.base_bg});

		&:hover {
			background-color: ${props => props.theme.accent_bg};
		}
	}

	& div {
		border: ${props => props.theme.base_border};
		position: absolute;
		z-index: 1;

		& button {
			width: 100%;
			border: none;
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
			<DropdownWrapper ref={this.ref}>
				<button onClick={this.toggleMenu}>
					<img draggable="false" src={this.props.children[this.state.activeOption].props.image}/>
					{this.props.children[this.state.activeOption].props.name}
				</button>
				{this.state.isMenuVisible &&
					<div>
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
	children: children_class_validator([DropdownItem], 1)
};

export { Checkbox, Dropdown, DropdownItem };