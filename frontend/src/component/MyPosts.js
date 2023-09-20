import { useState, useEffect } from "react";
import backend from "../utils/api";
import { Container, Title } from "./common";
import { Link } from "react-router-dom";

function Card({ post }) {
	const date = new Date("2023-09-19T14:25:22.057076+09:00");
	const formattedDate = date.toLocaleDateString();
	const formattedTime = date.toLocaleTimeString();
	return (
		<div className="py-3">
			<div className="text-white bg-neutral-700 p-5 rounded-xl">
				<h2 className="text-xl">{post.owner.username}</h2>
				<pre className="py-3">{post.content}</pre>
				{post.image && <img src={post.image} alt="" className="max-h-96" />}
				<p className="text-xs">
					{formattedTime} - {formattedDate}
				</p>
			</div>
		</div>
	);
}

export default function MyPosts() {
	const [posts, setPosts] = useState([]);

	const getPosts = () => {
		backend("get", "/user/posts/")
			.then((res) => {
				console.log(res);
				setPosts(res);
			})
			.catch((err) => {});
	};

	useEffect(() => {
		getPosts();
	}, []);

	return (
		<Container>
			<Title name="작성한 개시물" />
			<div className="max-w-3xl mx-auto">
				<div className="grid place-content-end">
					<Link to="/newpost" className="bg-indigo-700 text-white p-2 rounded-md">
						새 개시물
					</Link>
				</div>
				{posts.map((post) => {
					return <Card key={post.id} post={post} />;
				})}
			</div>
		</Container>
	);
}
