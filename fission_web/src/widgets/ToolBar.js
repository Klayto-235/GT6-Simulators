import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';


class ToolItemSeparator extends React.Component {
	render() {
		return <span/>;
	}
}

class ToolItemButton extends React.Component {
	render() {
		return (
			<button className={this.props.name ? " hasName" : ""} onClick={this.props.onClick}>
				<img src={this.props.image}/>
				{this.props.name}
			</button>
		);
	}
}

ToolItemButton.propTypes = {
	name: PropTypes.string,
	image: PropTypes.string,
	onClick: PropTypes.func
};

const ToolBarWrapper = styled.div`
	display: flex;
	align-items: center;

	& > span {
		align-self: stretch;
		margin: 5px 2px;
		border-left: ${props => props.theme.base_border};
		border-right: ${props => props.theme.secondary_border};
	}

	& > button {
		font-size: 0.9em;
		padding: 0;
		margin: 0 1px;
		border: ${props => props.theme.base_border};
		border-color: ${props => props.theme.base_bg};
		border-radius: 3px;

		&:hover {
			background-color: ${props => props.theme.accent_bg};
			border: ${props => props.theme.base_border};
		}

		& img {
			display: block;
		}

		&.hasName {
			padding: 0 calc(1px + 0.5em);
		}
	}

	&.vertical {
		flex-direction: column;

		& > span {
			margin: 2px 5px;
			border: unset;
			border-top: ${props => props.theme.base_border};
			border-bottom: ${props => props.theme.secondary_border};
		}

		& > button {
			margin: 1px 0;
		}
	}
`;

class ToolBar extends React.Component {
	render() {
		let index = -1;
		return (
			<ToolBarWrapper className={(this.props.className + (this.props.horizontal ? "" : " vertical"))}>
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
	children: function(props, propName, componentName) {
		const prop = props[propName];
	
		let error = null;
		React.Children.forEach(prop, function (child) {
			if (child.type !== ToolItemButton && child.type !== ToolItemSeparator)
				error = new Error('Children of type ' + componentName + ' should be of type ToolItemButton or ToolItemSeparator.');
		});
		return error;
	}
};

ToolBar.defaultProps = {
	horizontal: true
};

export { ToolBar, ToolItemButton, ToolItemSeparator };