import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { recursiveMap } from '../util';


const ToolItemBlank = styled.div`
	text-align: center;
`;

const ToolItemSeparator = styled.span`
	align-self: stretch;
	margin: 5px 8px;
	border-left: ${props => props.theme.secondary_border};
	border-right: ${props => props.theme.secondary_border};
	border-right-color: white;

	&.vertical {
		margin: 8px 5px;
		border: unset;
		border-top: ${props => props.theme.secondary_border};
		border-bottom: ${props => props.theme.secondary_border};
		border-bottom-color: white;
	}
`;

const ToolItemSpacer = styled.span``;

const ToolBarWrapper = styled.div`
	display: flex;
	align-items: center;

	&.vertical {
		flex-direction: column;
	}

	&.inline {
		display: inline-flex;
	}
`;

class ToolBar extends React.Component {
	render() {
		return (
			<ToolBarWrapper style={this.props.style}
			className={`${this.props.className ? this.props.className : ""} ${this.props.horizontal ? "" : "vertical"} ${this.props.inline ? "inline" : ""}`}>
				{this.props.horizontal ? this.props.children : recursiveMap(this.props.children, child => child.type == ToolItemSeparator ?
				React.cloneElement(child, {className: `vertical ${child.props.className ? child.props.className : ""}`}) : child)}
			</ToolBarWrapper>
		);
	}
}

ToolBar.propTypes = {
	horizontal: PropTypes.bool,
	inline: PropTypes.bool,
	children: PropTypes.node,
	className: PropTypes.string,
	style: PropTypes.object
};

ToolBar.defaultProps = {
	horizontal: true,
	inline: false
};

export { ToolBar, ToolItemSeparator, ToolItemSpacer, ToolItemBlank };