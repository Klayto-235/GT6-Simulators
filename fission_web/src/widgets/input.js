import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';


const CheckboxButton = styled.button`
	border: none;
	background-color: ${props => props.theme.base_bg};
	font-size: 0.9rem;
	padding: 0 0.2em 0 0;

	& span {
		display: inline-block;
		font-size: 0.9em;
		margin-right: 0.3em;
		padding-left: 0.1em;
		width: 0.9em;
		height: 1em;
		border-radius: 1px;
		border: ${props => props.theme.accent_border};
		background-color: ${props => props.theme.accent_bg};
	}

	&:hover span {
		background-color: ${props => props.theme.secondary_active};
	}

	& span.unchecked {
		color: ${props => props.theme.accent_bg};
	}
`;

class Checkbox extends React.Component {
	render() {
		return (
			<CheckboxButton onClick={this.props.onClick}>
				<span className={this.props.checked ? "" : "unchecked"}>✓</span>
				{this.props.name}
			</CheckboxButton>
		);
	}
}

Checkbox.propTypes = {
	name: PropTypes.string,
	checked: PropTypes.bool,
	onClick: PropTypes.func
};

export { Checkbox };