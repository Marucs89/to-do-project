import { ToDos } from "../../../../../schemas/to-do";

export function createMarkerForTask(bearbeiter: ToDos[0]["arbeiter"]) {
  const backgroundColors = bearbeiter.map((arbeiter) => {
    let markerColor;
    switch (arbeiter.name) {
      case "Marcus":
        markerColor = "rgb(21, 255, 0)";
        break;
      case "Finn":
        markerColor = "rgb(255, 9, 1)";
        break;
      case "Jonas":
        markerColor = "rgb(170, 170, 170)";
        break;
      case "Marcel":
        markerColor = "rgb(128, 0, 255)";
        break;
      default:
        markerColor = "";
    }
    return markerColor;
  });

  return backgroundColors.length > 1
    ? `linear-gradient(150deg, ${backgroundColors.join(",")})`
    : backgroundColors[0];
}
