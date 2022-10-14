import React from "react";


function childrenClassValidator(classList, minChildren=0) {
	return function(props, propName, componentName) {
		const prop = props[propName];
	
		let error = null;
		let num = 0;
		React.Children.forEach(prop, function (child) {
			num = num + 1;
			if (!classList.some(cls => cls === child.type))
				error = new Error("Children of type " + componentName + " should be of types: " + classList.map(cls => cls.name).join(", "));
		});
		if (num < minChildren)
			error = new Error("Type " + componentName + " requires at least " + minChildren + (minChildren == 1 ? " child" : " children"));

		return error;
	};
}

function recursiveMap(children, fn) {
	return React.Children.map(children, child => {
		if (!React.isValidElement(child)) {
			return child;
		}

		if (child.props.children) {
			child = React.cloneElement(child, {
				children: recursiveMap(child.props.children, fn)
			});
		}
	
		return fn(child);
	});
}

export { childrenClassValidator, recursiveMap };