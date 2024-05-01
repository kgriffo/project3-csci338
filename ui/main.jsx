async function main() {
    console.log("hello world");
  }
  
  window.onload=main

function FilmEntry({ id, title, description }) {
  return (
    <p>
      <a href={`/film/${id}`}>{title}</a>: {description}
    </p>
  );
}