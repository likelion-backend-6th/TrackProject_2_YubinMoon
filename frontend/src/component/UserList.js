import { useState, useEffect } from "react";
import backend from "../utils/api";
import { Container, Title } from "./common";

function UserBox({ user, get_users }) {
	const data = {
		class: user.following ? "bg-neutral-400" : "bg-blue-600",
		content: user.following ? "언팔로우" : "팔로우",
	};

	const follow = (e) => {
		e.preventDefault();
		backend("post", "/follow/", { user: user.pk })
			.then((res) => {
				console.log(res);
				get_users();
			})
			.catch((err) => {
				console.log(err);
			});
	};

	return (
		<div className="py-3">
			<div className="text-white bg-neutral-700 rounded-lg flex justify-between items-center">
				<h3 className="text-3xl pl-4">{user.username}</h3>
				<div className="p-4">
					<button onClick={follow} className={`${data.class} rounded-md p-1 text-lg`}>
						{data.content}
					</button>
				</div>
			</div>
		</div>
	);
}

export default function UserList() {
	const [users, setUsers] = useState([]);

	const get_users = () => {
		backend("get", "/users/")
			.then((res) => {
				console.log(res);
				setUsers(res);
			})
			.catch((err) => {});
	};

	useEffect(() => {
		get_users();
	}, []);

	return (
		<Container>
			<Title name="유저 리스트" />
			<div className="max-w-3xl mx-auto">
				{users.map((user) => {
					return <UserBox key={user.pk} user={user} get_users={get_users} />;
				})}
			</div>
		</Container>
	);
}
