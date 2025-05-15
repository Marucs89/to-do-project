export function getTopicIdByName(topicName: string) {
  switch (topicName) {
    case "Freizeit":
      return 1;
    case "Arbeit":
      return 2;
    case "Schule":
      return 3;
    case "Sport":
      return 4;
  }
}


