import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import backend from "../utils/api";

export default function Signup() {
	const navigate = useNavigate();

	const signup = (e) => {
		e.preventDefault();
		const formData = new FormData(e.target);
		const data = Object.fromEntries(formData);
		console.log(data);
		if (data.password1 !== data.password2) {
			alert("Password does not match!");
			return;
		}
		data.password = data.password1;
		backend("post", "/user/signup/", data)
			.then((res) => {
				navigate("/login");
			})
			.catch((err) => {});
	};

	return (
		<div className="max-w-xl container mx-auto pt-9">
			<form onSubmit={signup} className="text-white">
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
						<label htmlFor="password1" className="text-3xl">
							Password:
						</label>
						<input
							id="password1"
							type="text"
							name="password1"
							className="text-black bg-neutral-200 focus:bg-white p-2 w-full rounded-lg outline-none text-lg"
						/>
					</li>
					<li className="py-6">
						<label htmlFor="password2" className="text-3xl">
							Password check:
						</label>
						<input
							id="password2"
							type="text"
							name="password2"
							className="text-black bg-neutral-200 focus:bg-white p-2 w-full rounded-lg outline-none text-lg"
						/>
					</li>
				</ul>
				<input type="submit" value="Login" hidden />
			</form>
		</div>
	);
}
