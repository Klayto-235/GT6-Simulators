import posthtml from 'posthtml';
import posthtmlInlineAssets from 'posthtml-inline-assets';
import fs from 'fs';


fs.readFile("./dist/index.html", function (err, data) {
	if (err) return console.error(err);
	posthtml([
		posthtmlInlineAssets({
			cwd: "./dist",
			root: "./dist",
			error: "throw"
		})
	])
	.process(data.toString())
	.then((result) => fs.promises.writeFile("./dist/standalone.html", result.html));
});
