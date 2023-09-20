import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import backend from "../utils/api";

export default function Login() {
	const navigate = useNavigate();

	const login = (e) => {
		e.preventDefault();
		const formData = new FormData(e.target);
		const data = Object.fromEntries(formData);
		console.log(data);
		backend("post", "/user/login/", data)
			.then((res) => {
				console.log(res);
				navigate("/");
			})
			.catch((err) => {});
	};

	useEffect(() => {
		backend("get", "/user/")
			.then((res) => {
				console.log(res);
				navigate("/");
			})
			.catch((err) => {});
	}, []);
	return (
		<div className="max-w-xl container mx-auto pt-9">
			<form onSubmit={login} className="text-white">
				<ul>
					<li className="py-6">
						<label htmlFor="username" className="text-3xl">
							Usename:
						</label>
						<input
							id="username"
							type="text"
							name="username"
							className="text-black bg-neutral-200 focus:bg-white p-2 w-full rounded-lg outline-none text-lg"
						/>
					</li>
					<li className="py-6">
						<label htmlFor="password" className="text-3xl">
							Password:
						</label>
						<input
							id="password"
							type="text"
							name="password"
							className="text-black bg-neutral-200 focus:bg-white p-2 w-full rounded-lg outline-none text-lg"
						/>
					</li>
				</ul>
				<input type="submit" value="Login" hidden />
			</form>
		</div>
	);
}
