import React from "react";


function children_class_validator(classList) {
	return function(props, propName, componentName) {
		const prop = props[propName];
	
		let error = null;
		React.Children.forEach(prop, function (child) {
			if (!classList.some(cls => cls === child.type))
				error = new Error("Children of type " + componentName + " should be of types: " + classList.map(cls => cls.name).join(", "));
		});

		return error;
	};
}

export { children_class_validator };