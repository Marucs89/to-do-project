import MainScreen from "./components/MainScreen/MainScreen";

export enum Users {
  undefined = "undefined",
  Finn = "Finn",
  Marcel = "Marcel",
  Jonas = "Jonas",
  Marcus = "Marcus",
}

function App() {
  return (
    <>
      <MainScreen />
    </>
  );
}

export default App;
