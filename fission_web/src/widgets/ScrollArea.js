import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';


const ScrollAreaWrapper = styled.div`
	background-color: ${props => props.theme.accent_bg};
	border: ${props => props.theme.base_border};
	overflow: hidden;
`;

const ScrollAreaContentWrapper = styled.div`
	display: inline-block;
	transition: transform 0.2s;
	transform-origin: 0 0;
`;

class ScrollArea extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			contentPos:			[0, 0],
			clickContentPos:	[0, 0],
			clickPos:			[0, 0],
			dragging:			false,
			contentScaleLevel:	0,
			contentScalePos:	[0, 0]
		};

		this.ref = React.createRef();

		this.onMouseDown =	this.onMouseDown.bind(this);
		this.onMouseUp =	this.onMouseUp.bind(this);
		this.onMouseMove =	this.onMouseMove.bind(this);
		this.onWheel =		this.onWheel.bind(this);
	}

	componentDidMount() {
		this.ref.current.addEventListener('wheel', this.onWheel, { passive: false });
	}

	componentWillUnmount() {
		window.removeEventListener('mousemove', this.onMouseMove);
		window.removeEventListener('mouseup', this.onMouseUp);
		this.ref.current.removeEventListener('wheel', this.onWheel, { passive: false });
	}

	componentDidUpdate(prevProps, prevState) {
		if (prevState.dragging != this.state.dragging) {
			if (this.state.dragging) {
				window.addEventListener('mousemove', this.onMouseMove);
				window.addEventListener('mouseup', this.onMouseUp);
			}
			else {
				window.removeEventListener('mousemove', this.onMouseMove);
				window.removeEventListener('mouseup', this.onMouseUp);
			}
		}
		return null;
	}

	onMouseDown(event) {
		this.setState(state => {
			return {
				clickPos: [event.clientX, event.clientY],
				clickContentPos: state.contentPos,
				dragging: true
			};
		});
	}

	onMouseUp() {
		this.setState({dragging: false});
	}

	onMouseMove(event) {
		this.setState(state => {
			return {
				contentPos: [state.clickContentPos[0] + (event.clientX - state.clickPos[0]), state.clickContentPos[1] + (event.clientY - state.clickPos[1])]
			};
		});
	}

	onWheel(event) {
		event.preventDefault();
		const areaRect = this.ref.current.getBoundingClientRect();
		let magnify = (event.deltaY < 0 ? 1 : -1);
		let refPoint = event.deltaY > 0 ? [areaRect.width/2, areaRect.height/2] : [event.clientX - areaRect.x, event.clientY - areaRect.y];
		this.setState((state, props) => {
			if (state.contentScaleLevel + magnify > props.maxScaleLevel || state.contentScaleLevel + magnify < props.minScaleLevel) magnify = 0;
			refPoint = [refPoint[0] - state.contentPos[0] - state.contentScalePos[0], refPoint[1] - state.contentPos[1] - state.contentScalePos[1]];
			const scaleFactor = props.scaleBase ** magnify;
			return {
				contentScaleLevel: state.contentScaleLevel + magnify,
				contentScalePos: [state.contentScalePos[0] - refPoint[0]*(scaleFactor - 1), state.contentScalePos[1] - refPoint[1]*(scaleFactor - 1)]
			};
		});
	}

	render() {
		return (
			<ScrollAreaWrapper style={this.props.style} className={this.props.className} onMouseDown={this.onMouseDown} ref={this.ref}>
                <ScrollAreaContentWrapper style={{transform: `translate(${this.state.contentScalePos[0]}px, ${this.state.contentScalePos[1]}px)
				scale(${this.props.scaleBase ** this.state.contentScaleLevel})`,
				translate: `${this.state.contentPos[0]}px ${this.state.contentPos[1]}px`}}>
					{this.props.children}
				</ScrollAreaContentWrapper>
            </ScrollAreaWrapper>
		);
	}
}

ScrollArea.propTypes = {
	className:		PropTypes.string,
	style:			PropTypes.object,
	children:		PropTypes.node,
	scaleBase:		PropTypes.number,
	maxScaleLevel:	PropTypes.number,
	minScaleLevel:	PropTypes.number
};

ScrollArea.defaultProps = {
	className:		"",
	scaleBase:		2,
	maxScaleLevel:	2,
	minScaleLevel:	-2
};

export { ScrollArea };