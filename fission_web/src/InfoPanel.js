import React from 'react';
import InfoPlot from './InfoPlot';
import InfoText from './InfoText';


function InfoPanel() {
	return (
		<div className="infoPanel">
			<InfoPlot/>
			<InfoText/>
		</div>
	);
}

export default InfoPanel;