import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';


const ToolItemBlank = styled.div`
	& > * {
		display: block;
	}
`;

const ToolItemSeparator = styled.span``;

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
			<ToolBarWrapper style={this.props.style}
			className={`${this.props.className ? this.props.className : ""} ${this.props.horizontal ? "" : "vertical"} ${this.props.inline ? "inline" : ""}`}>
				{React.Children.map(this.props.children, child => (++index, React.cloneElement(child, {
					key: index
				})))}
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

export { ToolBar, ToolItemSeparator, ToolItemBlank };