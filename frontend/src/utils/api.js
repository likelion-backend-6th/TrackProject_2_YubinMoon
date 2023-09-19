const backend = async (operation, url, params, content_type = "application/json") => {
	let method = operation;
	let body = JSON.stringify(params);

	let _url = process.env.REACT_APP_API_SERVER_URL + url;
	if (method === "get" || method === "delete") {
		_url += "?" + new URLSearchParams(params);
	}

	let options = {
		method: method,
		credentials: "include",
	};
	console.log(options);
	if (content_type) {
		options["headers"] = {
			"Content-Type": content_type,
		};
		if (method !== "get" && method !== "delete") {
			options["body"] = body;
		}
	} else {
		if (method !== "get" && method !== "delete") {
			options["body"] = params;
		}
	}
	console.log(options);
	try {
		const response = await fetch(_url, options);

		if (response.status === 204) {
			// No content
			return;
		}

		const json = await response.json();

		if (response.status >= 200 && response.status < 300) {
			// 200 ~ 299
			return json;
		} else {
			console.log(json);
			throw response;
		}
	} catch (error) {
		throw error;
	}
};

export default backend;
