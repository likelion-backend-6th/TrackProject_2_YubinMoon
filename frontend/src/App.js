import {
	BrowserRouter,
	Routes,
	Route,
	useRouteError,
	useNavigate,
	Navigate,
} from "react-router-dom";
import { useEffect, useLayoutEffect } from "react";
import backend from "./utils/api";
import Layout from "./component/Layout";
import Main from "./component/Main";
import Login from "./component/Login";
import Signup from "./component/Signup";
import MyPosts from "./component/MyPosts";
import Posts from "./component/Posts";
import UserList from "./component/UserList";
import NewPost from "./component/NewPost";

function App() {
	return (
		<Routes>
			<Route path="/" element={<Layout />}>
				<Route path="/" element={<Main />}>
					<Route path="/" element={<UserList />} />
					<Route path="myposts" element={<MyPosts />} />
					<Route path="newpost" element={<NewPost />} />
					<Route path="posts" element={<Posts />} />
				</Route>
				<Route path="login" element={<Login />} />
				<Route path="signup" element={<Signup />} />
			</Route>
			<Route path="*" element={<Navigate to="/" />} />
		</Routes>
	);
}

export default App;
