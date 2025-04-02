import MainScreen from "./components/Overview/MainScreen/MainScreen";

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
      <MainScreen />
    </div>
  );
}

export default App;
