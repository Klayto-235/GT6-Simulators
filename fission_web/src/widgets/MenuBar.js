import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { childrenClassValidator } from '../util';


const MenuItemSeparator = styled.hr`
	border: ${props => props.theme.secondary_border};
	margin: 0.2em 5px;
`;

const MenuItemBaseStyle = styled.button`
	border: none;
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
			<MenuItemButtonStyle onClick={() => (this.props.onClick && this.props.onClick(), this.props.onClickButton())}onMouseEnter={this.props.onMouseEnter} tabIndex={-1}>
				<span className={this.props.checked ? "" : "hidden"}>✓</span>
				{this.props.name}
				<span>{this.props.hotkey}</span>
			</MenuItemButtonStyle>
		);
	}
}

MenuItemButton.propTypes = {
	onClick:		PropTypes.func,
	checked:		PropTypes.bool,
	name:			PropTypes.string,
	onMouseEnter:	PropTypes.func,
	hotkey:			PropTypes.string,
	onClickButton:	PropTypes.func
};

MenuItemButton.defaultProps = {
	checked: false
};

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
				<MenuItemMenuStyle onMouseEnter={this.props.onMouseEnter} tabIndex={-1}>
					<span>✓</span>
					{this.props.name}
					<span>▸</span>
				</MenuItemMenuStyle>
				{this.props.active &&
					<MenuContent onClickButton={this.props.onClickButton} parentRef={this.state.ref}>
						{this.props.children}
					</MenuContent>}
			</MenuItemMenuWrapper>
		);
	}
}

MenuItemMenu.propTypes = {
	name:			PropTypes.string,
	children:		childrenClassValidator([MenuItemMenu, MenuItemButton, MenuItemSeparator]),
	onMouseEnter:	PropTypes.func,
	active:			PropTypes.bool,
	onClickButton:	PropTypes.func
};

MenuItemMenu.defaultProps = {
	active: false
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
				{React.Children.map(this.props.children, child => (++index,
					child.type == MenuItemSeparator ?
					React.cloneElement(child, {
						key: index,
						onMouseEnter: this.onMouseEnterItem.bind(this, index),
						active: index == this.state.activeItem
					}) :
					React.cloneElement(child, {
						key: index,
						onMouseEnter: this.onMouseEnterItem.bind(this, index),
						active: index == this.state.activeItem,
						onClickButton: this.props.onClickButton
					})
				))}
			</MenuContentStyle>;
	}
}

MenuContent.propTypes = {
	children:		PropTypes.node,
	parentRef:		PropTypes.any,
	onMouseEnter:	PropTypes.func,
	onMouseLeave:	PropTypes.func,
	onClickButton:	PropTypes.func
};

const MenuHeader = styled.button`
	border: none;
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
				<MenuHeader className={this.props.visible ? "visible" : ""} onClick={this.props.onClick} tabIndex={-1}
					onMouseEnter={this.props.onMouseEnter}>{this.props.header}</MenuHeader>
				{this.props.visible && <MenuContent onClickButton={this.props.onClickButton}>{this.props.children}</MenuContent>}
			</MenuWrapper>
		);
	}
}

Menu.propTypes = {
	onClick:		PropTypes.func,
	onMouseEnter:	PropTypes.func,
	header:			PropTypes.string,
	visible:		PropTypes.bool,
	children:		childrenClassValidator([MenuItemMenu, MenuItemButton, MenuItemSeparator]),
	onClickButton:	PropTypes.func
};

Menu.defaultProps = {
	visible: false
};

const MenuBarHeadersWrapper = styled.div`
	display: inline-block;
`;

const MenuBarWrapper = styled.div`
	border-bottom: ${props => props.theme.secondary_border};
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
		this.onClickButton = this.onClickButton.bind(this);
	}

	toggleMenu() {
		this.setState(state => ({isMenuVisible: !state.isMenuVisible}));
	}

	setActiveMenu(menuIndex) {
		this.setState({activeMenu: menuIndex});
	}

	onClickOutside(event) {
		if (!this.ref?.current.contains(event.target)) {
			this.setState({isMenuVisible: false});
        }
	}

	onClickButton() {
		this.setState({isMenuVisible: false});
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
			<MenuBarWrapper className={this.props.className} style={this.props.style}>
				<MenuBarHeadersWrapper ref={this.ref}>
					{React.Children.map(this.props.children, child => (++index, React.cloneElement(child, {
						key: index,
						onClick: this.toggleMenu,
						onMouseEnter: this.setActiveMenu.bind(this, index),
						visible: this.state.activeMenu == index && this.state.isMenuVisible,
						onClickButton: this.onClickButton
					})))}
				</MenuBarHeadersWrapper>
			</MenuBarWrapper>
		);
	}
}

MenuBar.propTypes = {
	className:	PropTypes.string,
	style:		PropTypes.object,
	children:	childrenClassValidator([Menu])
};

export { MenuBar, Menu, MenuItemButton, MenuItemMenu, MenuItemSeparator };