import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';


class ReactorSlot extends React.Component {
    constructor(props) {
        super(props);

        this.onMouseDown = this.onMouseDown.bind(this);
    }

	onMouseDown(event) {
		event.stopPropagation();
	}

    render() {
        return (
            <button tabIndex={-1} onClick={this.props.onClick} onMouseDown={this.onMouseDown} className={this.props.checked ? "checked" : ""}/>
        );
    }
}

ReactorSlot.propTypes = {
	onClick:	PropTypes.func,
	checked:	PropTypes.bool
};

ReactorSlot.defaultProps = {
    onClick:    () => {},
	checked:    false
};

const ReactorBlockStyle = styled.div`
	padding: 0;
	margin: 1px;
    line-height: 0;
    display: inline-block;

    & > button {
        width: 48px;
        height: 48px;
        padding: 0;
        margin: 1px;
        border: ${props => props.theme.base_border};
        background-color: ${props => props.theme.base_bg};
        border-radius: 2px;

        &:hover {
            border: ${props => props.theme.selection_border_hover};
        }

        &.checked {
            border: ${props => props.theme.selection_border_active};
        }
    }
`;

class ReactorBlock extends React.Component {
    constructor(props) {
        super(props);
    }

	render() {
		return (
			<ReactorBlockStyle style={this.props.style} className={this.props.className}>
				<ReactorSlot onClick={this.props.onClick.bind(null, 0)} checked={this.props.checked == 0}/>
                <ReactorSlot onClick={this.props.onClick.bind(null, 1)} checked={this.props.checked == 1}/>
                <br/>
                <ReactorSlot onClick={this.props.onClick.bind(null, 2)} checked={this.props.checked == 2}/>
                <ReactorSlot onClick={this.props.onClick.bind(null, 3)} checked={this.props.checked == 3}/>
			</ReactorBlockStyle>
		);
	}
}

ReactorBlock.propTypes = {
	onClick:	PropTypes.func,
	checked:	PropTypes.number,
	className:	PropTypes.string,
	style:		PropTypes.object
};

ReactorBlock.defaultProps = {
	checked:    -1,
    onClick:    () => {}
};

export { ReactorBlock };