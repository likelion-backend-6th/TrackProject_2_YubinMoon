import { useState, useEffect } from "react";
import backend from "../utils/api";
import { Container, Title } from "./common";

function UserBox({ username }) {}

export default function UserList() {
	useEffect(() => {
		backend("get", "/users/")
			.then((res) => {
				console.log(res);
			})
			.catch((err) => {});
	}, []);

	return (
		<Container>
			<Title name="유저 리스트" />
		</Container>
	);
}
