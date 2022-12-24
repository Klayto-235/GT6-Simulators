import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import assets from '../assets.js';


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
            <button tabIndex={-1} onClick={this.props.onClick} onMouseDown={this.onMouseDown} className={this.props.checked ? "checked" : ""}
					style={{backgroundColor: this.props.color}}>
				<span style={{width: 60*this.props.progress, height: this.props.showProgress ? 10 : 0}}/>
				<span style={{width: 60 - 60*this.props.progress, height: this.props.showProgress ? 10 : 0}}/>
				<span>{this.props.label1}</span>
				<span>{this.props.label2}</span>
				<span>{this.props.rod !== "None" && this.props.rod}</span>
				{this.props.rod !== "None" && <img draggable="false" src={assets.topImages[this.props.rod]}/>}
			</button>
        );
    }
}

ReactorSlot.propTypes = {
	onClick:		PropTypes.func,
	checked:		PropTypes.bool,
	showProgress:	PropTypes.bool,
	progress:		PropTypes.number,
	rod:			PropTypes.string,
	label1:			PropTypes.string,
	label2:			PropTypes.string,
	color:			PropTypes.oneOfType([PropTypes.func, PropTypes.string])
};

ReactorSlot.defaultProps = {
    onClick:    	() => {},
	checked:    	false,
	showProgress:	true,
	progress:		0,
	rod:			"None",
	label1:			"",
	label2:			"",
	color:			props => props.theme.base_bg
};

const ReactorBlockStyle = styled.div`
	padding: 0;
	margin: 1px;
    line-height: 0;
    display: inline-block;
	position: relative;
	z-index: 0;

	& > span:nth-child(1) {
		font-size: 10px;
		position: absolute;
		line-height: 0.9;
		text-align: left;
		width: 59px;
		left: 2px;
		top: 2px;
		background-color: rgba(150, 150, 150, 0.2745);
		z-index: 1;
		padding-left: 1px;
	}

	& > span:nth-child(2) {
		font-size: 10px;
		position: absolute;
		line-height: 0.9;
		text-align: right;
		width: 59px;
		right: 2px;
		top: 2px;
		background-color: rgba(150, 150, 150, 0.2745);
		z-index: 1;
		padding-right: 1px;
	}

    & > button {
        width: 62px;
        height: 62px;
        padding: 0;
        margin: 1px;
        border: ${props => props.theme.base_border};
        border-radius: 2px;
		position: relative;
		z-index: 0;

        &:hover {
            border: ${props => props.theme.selection_border_hover};
        }

        &.checked {
            border: ${props => props.theme.selection_border_active};
        }

		& > span:nth-child(1) {
			border-bottom-left-radius: 2px;
			background-color: #d2ffd2;
			position: absolute;
			left: 0;
			bottom: 0;
		}

		& > span:nth-child(2) {
			border-bottom-right-radius: 1px;
			background-color: #ffd2d2;
			position: absolute;
			right: 0;
			bottom: 0;
		}

		& > span:nth-child(3) {
			font-size: 10px;
			position: absolute;
			right: 1px;
			bottom: 0;
			line-height: 0.8;
		}

		& > span:nth-child(4) {
			font-size: 10px;
			position: absolute;
			right: 1px;
			bottom: 11px;
			line-height: 0.8;
		}

		& > span:nth-child(5) {
			font-size: 10px;
			position: absolute;
			right: 0px;
			top: 13px;
			line-height: 0.8;
			width: 60px;
			text-align: center;
		}

		& > img {
			width: 16px;
			position: absolute;
			top: 22px;
			left: 22px;
		}
    }
`;

class ReactorBlock extends React.Component {
    constructor(props) {
        super(props);
    }

	render() {
		let hasCoolant = this.props.coolant !== "None";
		let color = hasCoolant ? assets.coolantColors[this.props.coolant] : (props => props.theme.base_bg);
		return (
			<ReactorBlockStyle style={this.props.style} className={this.props.className}>
			<span style={{height: hasCoolant ? 10 : 0}}>{hasCoolant && this.props.coolant}</span>
			<span style={{height: hasCoolant ? 10 : 0}}>{this.props.label}</span>
				<ReactorSlot onClick={this.props.onClick.bind(null, 0)} checked={this.props.checked == 0} rod={this.props.rods[0]}
					showProgress={this.props.showProgress[0]} progress={this.props.progress[0]} label1={this.props.labels1[0]}
					label2={this.props.labels2[0]} color={color}/>
                <ReactorSlot onClick={this.props.onClick.bind(null, 1)} checked={this.props.checked == 1} rod={this.props.rods[1]}
					showProgress={this.props.showProgress[1]} progress={this.props.progress[1]} label1={this.props.labels1[1]}
					label2={this.props.labels2[1]} color={color}/>
                <br/>
                <ReactorSlot onClick={this.props.onClick.bind(null, 2)} checked={this.props.checked == 2} rod={this.props.rods[2]}
					showProgress={this.props.showProgress[2]} progress={this.props.progress[2]} label1={this.props.labels1[2]}
					label2={this.props.labels2[2]} color={color}/>
                <ReactorSlot onClick={this.props.onClick.bind(null, 3)} checked={this.props.checked == 3} rod={this.props.rods[3]}
					showProgress={this.props.showProgress[3]} progress={this.props.progress[3]} label1={this.props.labels1[3]}
					label2={this.props.labels2[3]} color={color}/>
			</ReactorBlockStyle>
		);
	}
}

ReactorBlock.propTypes = {
	onClick:		PropTypes.func,
	checked:		PropTypes.number,
	className:		PropTypes.string,
	style:			PropTypes.object,
	coolant:		PropTypes.string,
	label:			PropTypes.string,
	showProgress:	PropTypes.arrayOf(PropTypes.bool),
	progress:		PropTypes.arrayOf(PropTypes.number),
	rods:			PropTypes.arrayOf(PropTypes.string),
	labels1:		PropTypes.arrayOf(PropTypes.string),
	labels2:		PropTypes.arrayOf(PropTypes.string)
};

ReactorBlock.defaultProps = {
	checked:		-1,
    onClick:		() => {},
	coolant:		"None",
	label:			"",
	showProgress:	[false, false, false, false],
	progress:		[0, 0, 0, 0],
	rods:			["None", "None", "None", "None"],
	labels1:		["", "", "", ""],
	labels2:		["", "", "", ""]
};

export { ReactorBlock };