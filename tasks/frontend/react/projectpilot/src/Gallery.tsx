// 1. The Child Component (Not exported, only used inside this file)
function Profile() {
  return (
    <img
      src="https://react.dev/images/docs/scientists/MK3eW3As.jpg"
      alt="Katherine Johnson"
    />
  );
}

// 2. The Parent Component (Exported so the rest of the app can see it)
export default function Gallery() {
  return (
    <section>
      <h2>Amazing scientists</h2>
      <Profile />
      <Profile />
      <Profile />
    </section>
  );
}