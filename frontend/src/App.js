import { BrowserRouter, Routes, Route, useRouteError, useNavigate } from "react-router-dom";
import { useEffect, useLayoutEffect } from "react";
import backend from "./utils/api";
import Layout from "./component/Layout";
import Main from "./component/Main";
import Login from "./component/Login";
import Signup from "./component/Signup";

function App() {
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<Layout />}>
					<Route index element={<Main />} />
					<Route path="login" element={<Login />} />
					<Route path="signup" element={<Signup />} />
				</Route>
			</Routes>
		</BrowserRouter>
	);
}

export default App;
