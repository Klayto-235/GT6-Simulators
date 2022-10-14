import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { childrenClassValidator, recursiveMap } from '../util';
import { Button as ToolItemButton } from './input';


const ToolItemBlank = styled.div`
	& > * {
		display: block;
	}
`;

const ToolItemSeparator = styled.span``;

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
				{recursiveMap(this.props.children, child => (++index,
				(child.type == ToolItemButton && (child.props?.group == this.props?.id)) ? React.cloneElement(child, {
					key: index,
					onClick: this.onClick.bind(this, index),
					checked: this.state.activeButton == index
				}) : child))}
			</>
		);
	}
}

ToolBarButtonGroup.propTypes = {
	children: childrenClassValidator([ToolItemSeparator, ToolItemButton, ToolItemBlank]),
	id: PropTypes.number
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

	&.vertical {
		flex-direction: column;

		& > span {
			margin: 2px 5px;
			border: unset;
			border-top: ${props => props.theme.secondary_border};
			border-bottom: ${props => props.theme.secondary_border};
			border-bottom-color: white;
		}
	}

	&.inline {
		display: inline-flex;
	}
`;

class ToolBar extends React.Component {
	render() {
		let index = -1;
		return (
			<ToolBarWrapper className={(this.props.className + (this.props.horizontal ? "" : " vertical") +
			(this.props.inline ? " inline" : ""))}>
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
	inline: PropTypes.bool,
	children: childrenClassValidator([ToolItemSeparator, ToolItemButton, ToolBarButtonGroup, ToolItemBlank])
};

ToolBar.defaultProps = {
	horizontal: true,
	inline: false
};

export { ToolBar, ToolItemButton, ToolItemSeparator, ToolBarButtonGroup, ToolItemBlank };