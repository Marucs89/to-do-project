import ToDoOverview from "./components/Overview/MainScreen/MainScreen";

export enum Users {
  undefined = "undefined",
  Finn = "Finn",
  Marcel = "Marcel",
  Jonas = "Jonas",
  Marcus = "Marcus",
}

function App() {
  return (
    <div>
      <ToDoOverview />
    </div>
  );
}

export default App;
