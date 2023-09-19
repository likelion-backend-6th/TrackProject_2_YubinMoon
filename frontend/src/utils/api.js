const backend = async (operation, url, params) => {
	let method = operation;
	let content_type = "application/json";
	let body = JSON.stringify(params);

	let _url = process.env.REACT_APP_API_SERVER_URL + url;
	if (method === "get" || method === "delete") {
		_url += "?" + new URLSearchParams(params);
	}

	let options = {
		method: method,
		headers: {
			"Content-Type": content_type,
		},
		credentials: "include",
	};

	if (method !== "get" && method !== "delete") {
		options["body"] = body;
	}

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
