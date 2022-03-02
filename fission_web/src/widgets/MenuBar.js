import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';


function menu_children_validator(props, propName, componentName) {
	const prop = props[propName];

	let error = null;
	React.Children.forEach(prop, function (child) {
		if (child.type !== MenuItemButton && child.type !== MenuItemSeparator && child.type !== MenuItemMenu)
			error = new Error('Children of type ' + componentName + ' should be of type MenuItemButton, MenuItemSeparator, or MenuItemMenu.');
	});
	return error;
}

const MenuItemSeparator = styled.hr`
	margin: 0;
	border: ${props => props.theme.base_border};
	margin: 0.2em 5px;
`;

const MenuItemMenuWrapper = styled.div`
	position: relative;

	& > button {
		border: none;
		font-size: 0.9rem;
		padding: 0.3em 10px 0.3em 5px;
		background-color: inherit;
		display: block;
		text-align: left;
		width: 100%;

		&:hover {
			background-color: ${props => props.theme.base_active};
		}

		& span:first-child {
			padding: 0 0.4em;
			visibility: hidden;
		}

		& span:last-child {
			float: right;
			position: relative;
			bottom: 1px;
		}
	}
`;

class MenuItemMenu extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			isMenuContentVisible: false,
			ref: undefined
		};
		this.ref = React.createRef();

		this.showMenuContent = this.showMenuContent.bind(this);
		this.hideMenuContent = this.hideMenuContent.bind(this);
	}

	showMenuContent() {
		this.setState({isMenuContentVisible: true});
	}

	hideMenuContent() {
		this.setState({isMenuContentVisible: false});
	}

	componentDidMount() {
		this.setState({ref: this.ref});
	}

	render() {
		return (
			<MenuItemMenuWrapper ref={this.ref}>
				<button onMouseEnter={this.showMenuContent} onMouseLeave={this.hideMenuContent}>
					<span>✓</span>
					{this.props.name}
					<span>▸</span>
				</button>
				{this.state.isMenuContentVisible &&
					<MenuContent onMouseEnter={this.showMenuContent} onMouseLeave={this.hideMenuContent} parentRef={this.state.ref}>
						{this.props.children}
					</MenuContent>}
			</MenuItemMenuWrapper>
		);
	}
}

MenuItemMenu.propTypes = {
	name: PropTypes.string,
	children: menu_children_validator
};

const MenuItemButtonStyle = styled.button`
	border: none;
	font-size: 0.9rem;
	padding: 0.3em 10px 0.3em 5px;
	background-color: inherit;
	display: block;
	text-align: left;
	width: 100%;

	&:hover {
		background-color: ${props => props.theme.base_active};
	}

	& span:first-child {
		padding: 0 0.4em;
	}

	& .hidden {
		visibility: hidden;
	}
`;

class MenuItemButton extends React.Component {
	render() {
		return (
			<MenuItemButtonStyle onClick={this.props.onClick}>
				<span className={this.props.checked ? "" : "hidden"}>✓</span>
				{this.props.name}
			</MenuItemButtonStyle>
		);
	}
}

MenuItemButton.propTypes = {
	onClick: PropTypes.func,
	checked: PropTypes.bool,
	name: PropTypes.string
};

MenuItemButton.defaultProps = {
	checked: false
};

const MenuContentStyle = styled.div`
	background-color: ${props => props.theme.accent_bg};
	border: ${props => props.theme.accent_border};
	position: absolute;
	z-index: 1;
	min-width: 10em;
	padding: 0.2em 0;
	
	& .subMenuRight {
		left: calc(100% - 3px);
		top: 0;
	}
	
	& .subMenuLeft {
		right: calc(100% - 3px);
		top: 0;
	}
`;

class MenuContent extends React.Component {
	constructor(props) {
		super(props);

		this.state = {positionClass: typeof this.props.parentRef == "undefined" ? "" : "subMenuRight"};
		this.ref = React.createRef();
	}

	componentDidMount() {
		if (typeof this.props.parentRef != "undefined") {
			let viewportWidth = document.documentElement.clientWidth;
			let parentRect = this.props.parentRef.current.getBoundingClientRect();
			let rect = this.ref.current.getBoundingClientRect();
			
			if ((rect.right > viewportWidth && parentRect.left >= rect.width) || parentRect.right > viewportWidth)
				this.setState({positionClass: "subMenuLeft"});
		}
	}

	render() {
		return <MenuContentStyle ref={this.ref} className={this.state.positionClass}
			onMouseEnter={this.props.onMouseEnter} onMouseLeave={this.props.onMouseLeave}>
				{this.props.children}
			</MenuContentStyle>;
	}
}

MenuContent.propTypes = {
	children: PropTypes.any,
	parentRef: PropTypes.any,
	onMouseEnter: PropTypes.func,
	onMouseLeave: PropTypes.func
};

const MenuHeader = styled.button`
	border: none;
	font-size: 0.9rem;
	padding: 0.2em 0.5em;
	background-color: inherit;
	transition: background-color 0.2s;

	&.visible {
		background-color: ${props => props.theme.base_active};
	}
`;

const MenuWrapper = styled.div`
	display: inline-block;
`;

class Menu extends React.Component {
	render() {
		return (
			<MenuWrapper>
				<MenuHeader className={this.props.visible ? "visible" : ""} onClick={this.props.onClick}
					onMouseEnter={this.props.onMouseEnter}>{this.props.header}</MenuHeader>
				{this.props.visible && <MenuContent>{this.props.children}</MenuContent>}
			</MenuWrapper>
		);
	}
}

Menu.propTypes = {
	onClick: PropTypes.func,
	onMouseEnter: PropTypes.func,
	header: PropTypes.string,
	visible: PropTypes.bool,
	children: menu_children_validator
};

const MenuBarWrapper = styled.div`
	border-bottom: ${props => props.theme.base_border};
	white-space: nowrap;
`;

class MenuBar extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			isMenuVisible: false,
			activeMenu: -1
		};

		this.toggleMenu = this.toggleMenu.bind(this);
	}

	toggleMenu() {
		this.setState(prevState => ({
			isMenuVisible: !prevState.isMenuVisible
		}));
	}

	setActiveMenu(menuIndex) {
		this.setState({activeMenu: menuIndex});
	}

	render() {
		let index = 0;
		return (
			<MenuBarWrapper className={typeof this.props.className == "undefined" ? "" : this.props.className}>
				{React.Children.map(this.props.children, child => React.cloneElement(child, {
					key: index++,
					onClick: this.toggleMenu,
					onMouseEnter: this.setActiveMenu.bind(this, index),
					visible: this.state.activeMenu == index && this.state.isMenuVisible
				}))}
			</MenuBarWrapper>
		);
	}
}

MenuBar.propTypes = {
	className: PropTypes.string,
	children: function (props, propName, componentName) {
		const prop = props[propName];
	
		let error = null;
		React.Children.forEach(prop, function (child) {
			if (child.type !== Menu)
				error = new Error('Children of type ' + componentName + ' should be of type Menu.');
		});
		return error;
	}
};

export { MenuBar, Menu, MenuItemButton, MenuItemMenu, MenuItemSeparator };