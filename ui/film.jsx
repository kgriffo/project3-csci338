import React from "react";
import { createRoot } from "react-dom/client";

// ChatGPT was used heavily when writing this. It still doesn't work perfectly,
// but at least it displays the list properly (just not the individual movies when clicked). 
async function fetchFilmData() {
	try {
		const filmId = window.location.pathname.split("/").pop();
		if (filmId) {
			const response = await fetch(`/api/v1/film/${filmId}`);
			if (!response.ok) {
				throw new Error("Failed to fetch film data");
			}
			return await response.json();
		} else {
			const response = await fetch("/api/v1/films");
			if (!response.ok) {
				throw new Error("Failed to fetch film list");
			}
			return await response.json();
		}
	} catch (error) {
		console.error(error);
		return null;
	}
}

async function deleteFilm() {
	const filmId = window.location.pathname.split("/").pop();
	const response = await fetch(`/api/v1/film/${filmId}`, {
		method: 'DELETE'
	});
	window.location.href = "/";
}

async function main() {
	const filmData = await fetchFilmData();
	const rootElt = document.getElementById("app");
	const root = createRoot(rootElt);
	if (Array.isArray(filmData)) {
		root.render(
			<div>
				<ul>
					{filmData.map((film) => (
						<li key={film.id}>
							<p>
								<a href={`/film/${film.id}`}>{film.title}</a>: {film.description}
							</p>
						</li>
					))}
				</ul>
			</div>
		);
	} else {
		root.render(
			<div>
				<h1>{filmData.title}</h1>
				<p>{filmData.description}</p>
				<a href={deleteFilm()}>Delete</a>
				<a href="/">Back to list</a>
			</div>
		);
	}
}

window.onload = main;

