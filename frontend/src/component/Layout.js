import { Outlet, Link, useNavigate } from "react-router-dom";
import useStore from "../utils/store";
import backend from "../utils/api";

export default function Layout() {
	const { login, setLogin } = useStore();
	const navigate = useNavigate();

	const logout = () => {
		backend("get", "/user/logout/")
			.then((res) => {
				console.log(res);
				setLogin(null);
				navigate("/login");
			})
			.catch((err) => {});
	};
	return (
		<div className="bg-indigo-900 h-[100vh] from-neutral-900 to-stone-800  bg-gradient-to-b">
			<div className="border-b-2 border-neutral-700 py-3 text-white">
				<ul className="max-w-6xl container mx-auto flex justify-between">
					<li>
						<Link to="/">
							<div className="flex items-center text-3xl">
								<img src="/logo.png" alt="logo" className="h-16" />
								<h1>follow</h1>
							</div>
						</Link>
					</li>
					<li>
						<ul className="h-full flex text-3xl py-2">
							{login ? (
								<li className="h-full px-2 mx-2 items-center just hover:border-b-2 border-neutral-300">
									<button onClick={logout} className="h-full flex flex-col justify-center">
										<h1>Logout</h1>
									</button>
								</li>
							) : (
								<>
									<li className="h-full px-2 mx-2 items-center just hover:border-b-2 border-neutral-300">
										<Link to="/login" className="h-full flex flex-col justify-center">
											<h1>Login</h1>
										</Link>
									</li>
									<li className="h-full px-2 mx-2 items-center just hover:border-b-2 border-neutral-300">
										<Link to="/signup" className="h-full flex flex-col justify-center">
											<h1>SignUp</h1>
										</Link>
									</li>
								</>
							)}
						</ul>
					</li>
				</ul>
			</div>
			<Outlet />
		</div>
	);
}
