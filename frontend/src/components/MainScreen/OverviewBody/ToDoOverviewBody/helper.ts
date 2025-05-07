import { ToDos } from "../../../../schemas/to-do";

export function createMarkerForTask(bearbeiter: ToDos[0]["arbeiter"]) {
  const backgroundColors = bearbeiter.map((arbeiter) => {
    let markerColor;

    switch (arbeiter.name) {
      case "Marcus":
        markerColor = "rgb(5, 177, 199)";
        break;
      case "Finn":
        markerColor = "rgb(163, 5, 0)";
        break;
      case "Jonas":
        markerColor = "rgb(208, 4, 133)";
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
