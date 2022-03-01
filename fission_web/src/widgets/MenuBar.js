import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';


class MenuContent extends React.Component {

}

const MenuButton = styled.button`
	border: none;
	font-size: 0.9rem;
	padding: 0.2em 0.5em;
	background-color: inherit;
	transition: background-color 0.2s;

	&.visible {
		background-color: ${props => props.theme.button_active};
	}
`;

const MenuWrapper = styled.div`
	display: inline-block;
`;

class Menu extends React.Component {
	render() {
		return (
			<MenuWrapper>
				<MenuButton className={this.props.visible ? "visible" : ""} onClick={this.props.onClick}
					onMouseEnter={this.props.onMouseEnter}>{this.props.header}</MenuButton>
				{this.visible && <MenuContent>{typeof this.props.items == "undefined" ? [] : this.props.items}</MenuContent>}
			</MenuWrapper>
		);
	}
}

Menu.propTypes = {
	onClick: PropTypes.func.isRequired,
	onMouseEnter: PropTypes.func.isRequired,
	header: PropTypes.string.isRequired,
	items: PropTypes.array.isRequired,
	visible: PropTypes.bool.isRequired
};

const MenuBarWrapper = styled.div`
	background-color: ${props => props.theme.bg_menu};
	border-bottom: 1px solid ${props => props.theme.border};
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
		return (
			<MenuBarWrapper className={typeof this.props.className == "undefined" ? "" : this.props.className}>
				{this.props.menus.map((menu, index) => <Menu
					key={index}
					onClick={this.toggleMenu}
					onMouseEnter={this.setActiveMenu.bind(this, index)}
					visible={this.state.activeMenu == index && this.state.isMenuVisible}
					header={menu.header}
					items={menu.items}
				/>)}
			</MenuBarWrapper>
		);
	}
}

MenuBar.propTypes = {
	className: PropTypes.string,
	menus: PropTypes.array.isRequired
};

export default MenuBar;