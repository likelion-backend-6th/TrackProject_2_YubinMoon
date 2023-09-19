import { BrowserRouter, Routes, Route, useRouteError, useNavigate, Outlet } from "react-router-dom";
import { useState } from "react";
import backend from "../utils/api";
import MyPosts from "./MyPosts";
import useStore from "../utils/store";

export default function Main() {
	const navigate = useNavigate();
	const { setLogin } = useStore();

	useState(() => {
		console.log("asdf");
		backend("get", "/user/")
			.then((res) => {
				setLogin(res);
			})
			.catch((err) => {
				if (err.status === 403) {
					navigate("/login");
				}
			});
	}, []);

	return <Outlet />;
}
