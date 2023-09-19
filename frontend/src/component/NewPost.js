import { useNavigate } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import backend from "../utils/api";
import { Container, Title } from "./common";
import { Link } from "react-router-dom";

export default function NewPost() {
	const [imgFile, setImgFile] = useState("");
	const [sendFile, setSendFile] = useState("");
	const [binaryFile, setBinaryFile] = useState("");
	const imgRef = useRef();
	const navigate = useNavigate();

	const saveImgFile = () => {
		const file = imgRef.current.files[0];
		setSendFile(file);
		const reader = new FileReader();
		if (file) {
			reader.readAsDataURL(file);
			reader.onloadend = () => {
				setImgFile(reader.result);
			};
		}
	};

	const createPost = (e) => {
		e.preventDefault();
		const formData = new FormData(e.target);
		formData.append("image", sendFile);
		backend("post", "/post/", formData, null)
			.then((res) => {
				console.log(res);
				navigate("/myposts");
			})
			.catch((err) => {});
	};

	return (
		<Container>
			<Title name="새 개시물" />
			<div className="max-w-3xl mx-auto">
				<form onSubmit={createPost} encType="multipart/form-data">
					<div className="py-3">
						<div className="grid place-content-end">
							<input
								type="submit"
								value="작성 완료"
								className="bg-indigo-700 text-white p-2 rounded-md"
							/>
						</div>
						<label className="text-white">
							<h3 className="text-3xl mb-4">내용</h3>
							<div className="p-4 bg-neutral-700 w-full rounded-lg">
								<textarea
									name="content"
									className=" resize-none outline-none w-full bg-transparent"
									rows="5"
								/>
							</div>
						</label>
					</div>
					<div className="py-3">
						<div className="p-4 bg-neutral-700 w-full rounded-lg">
							<label className="text-indigo-500 hover:text-green-500">
								{imgFile && <img src={imgFile} />}
								<h3 className="text-3xl text-center">{imgFile ? "이미지 변경" : "이미지 추가"}</h3>
								<input
									className="hidden"
									type="file"
									accept="image/*"
									id="image"
									onChange={saveImgFile}
									ref={imgRef}
								/>
							</label>
						</div>
					</div>
				</form>
			</div>
		</Container>
	);
}
