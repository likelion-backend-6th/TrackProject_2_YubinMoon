import { BrowserRouter, Routes, Route, useRouteError, useNavigate } from "react-router-dom";
import { useState } from "react";
import backend from "../utils/api";
import UserList from "./UserList";
import useStore from "../utils/store";

export default function Main() {
	const navigate = useNavigate();
	const { login, setLogin } = useStore();

	useState(() => {
		console.log("asdf");
		backend("get", "/user/")
			.then((res) => {
				setLogin(res);
				console.log(res);
			})
			.catch((err) => {
				if (err.status === 403) {
					navigate("/login");
				}
			});
	}, []);

	return (
		<Routes>
			<Route path="/" element={<UserList />} />
		</Routes>
	);
}
