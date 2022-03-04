import { Parcel } from '@parcel/core';
import posthtml from 'posthtml';
import posthtmlInlineAssets from 'posthtml-inline-assets';
import fs from 'fs';
import path from 'path';


async function build() {
	try {
		const files = await fs.promises.readdir("dist");
		for (const file of files) {
			fs.unlink(path.join("dist", file), () => {});
		}
	} catch(err) {0;}

	let bundler = new Parcel({
		entries: "src/index.html",
		defaultConfig: "@parcel/config-default",
		mode: "production",
		env: {NODE_ENV: "production"},
		additionalReporters: [{
			packageName: "@parcel/reporter-cli",
			resolveFrom: "./build.js"
		},{
			packageName: "@parcel/reporter-bundle-analyzer",
			resolveFrom: "./build.js"
		}]
	});

	try {
		await bundler.run();
	}
	catch (err) {
		return;
	}

	try {
		const data = await fs.promises.readFile("./dist/index.html");

		posthtml([
			posthtmlInlineAssets({
				cwd: "./dist",
				root: "./dist",
				error: "throw"
			})
		])
		.process(data.toString())
		.then((result) => fs.promises.writeFile("./dist/standalone.html", result.html));
	}
	catch(err) {
		return console.error(err);
	}
}

build();
