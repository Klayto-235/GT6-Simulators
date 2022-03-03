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

const MenuItemBaseStyle = styled.button`
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

	& span:last-child {
		float: right;
		margin-left: 1em;
	}
`;

const MenuItemMenuStyle = styled(MenuItemBaseStyle)`
	& span:first-child {
		visibility: hidden;
	}

	& span:last-child {
		position: relative;
		bottom: 1px;
	}
`;

const MenuItemMenuWrapper = styled.div`
	position: relative;
`;

class MenuItemMenu extends React.Component {
	constructor(props) {
		super(props);

		this.state = {ref: undefined};
		this.ref = React.createRef();
	}

	componentDidMount() {
		this.setState({ref: this.ref});
	}

	render() {
		return (
			<MenuItemMenuWrapper ref={this.ref}>
				<MenuItemMenuStyle onMouseEnter={this.props.onMouseEnter}>
					<span>✓</span>
					{this.props.name}
					<span>▸</span>
				</MenuItemMenuStyle>
				{this.props.active &&
					<MenuContent parentRef={this.state.ref}>
						{this.props.children}
					</MenuContent>}
			</MenuItemMenuWrapper>
		);
	}
}

MenuItemMenu.propTypes = {
	name: PropTypes.string,
	children: menu_children_validator,
	onMouseEnter: PropTypes.func,
	active: PropTypes.bool
};

const MenuItemButtonStyle = styled(MenuItemBaseStyle)`
	& span:last-child {
		color: ${props => props.theme.secondary_fg};
	}

	& .hidden {
		visibility: hidden;
	}
`;

class MenuItemButton extends React.Component {
	render() {
		return (
			<MenuItemButtonStyle onClick={this.props.onClick} onMouseEnter={this.props.onMouseEnter}>
				<span className={this.props.checked ? "" : "hidden"}>✓</span>
				{this.props.name}
				<span>{this.props.hotkey}</span>
			</MenuItemButtonStyle>
		);
	}
}

MenuItemButton.propTypes = {
	onClick: PropTypes.func,
	checked: PropTypes.bool,
	name: PropTypes.string,
	onMouseEnter: PropTypes.func,
	hotkey: PropTypes.string
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
	width: max-content;
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

		this.state = {
			positionClass: typeof this.props.parentRef == "undefined" ? "" : "subMenuRight",
			activeItem: -1
		};
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

	onMouseEnterItem(itemIndex) {
		this.setState({activeItem: itemIndex});
	}

	render() {
		let index = -1;
		return <MenuContentStyle ref={this.ref} className={this.state.positionClass}
			onMouseEnter={this.props.onMouseEnter} onMouseLeave={this.props.onMouseLeave}>
				{React.Children.map(this.props.children, child => (++index, React.cloneElement(child, {
					key: index,
					onMouseEnter: this.onMouseEnterItem.bind(this, index),
					active: index == this.state.activeItem
				})))}
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

const MenuBarHeadersWrapper = styled.div`
	display: inline-block;
`;

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
		this.ref = React.createRef();

		this.toggleMenu = this.toggleMenu.bind(this);
		this.onClickOutside = this.onClickOutside.bind(this);
	}

	toggleMenu() {
		this.setState(prevState => ({
			isMenuVisible: !prevState.isMenuVisible
		}));
	}

	setActiveMenu(menuIndex) {
		this.setState({activeMenu: menuIndex});
	}

	onClickOutside(event) {
		if (this.ref && !this.ref.current.contains(event.target)) {
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
			<MenuBarWrapper className={typeof this.props.className == "undefined" ? "" : this.props.className}>
				<MenuBarHeadersWrapper ref={this.ref}>
					{React.Children.map(this.props.children, child => (++index, React.cloneElement(child, {
						key: index,
						onClick: this.toggleMenu,
						onMouseEnter: this.setActiveMenu.bind(this, index),
						visible: this.state.activeMenu == index && this.state.isMenuVisible
					})))}
				</MenuBarHeadersWrapper>
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