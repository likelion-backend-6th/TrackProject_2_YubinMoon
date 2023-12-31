export function Container({ children }) {
	return (
		<div className="xl:max-w-6xl container mx-auto py-11">
			<div>{children}</div>
		</div>
	);
}

export function Title({ name }) {
	return (
		<div className="ml-10 mb-4">
			<h1 className="text-white text-4xl">{name}</h1>
		</div>
	);
}
