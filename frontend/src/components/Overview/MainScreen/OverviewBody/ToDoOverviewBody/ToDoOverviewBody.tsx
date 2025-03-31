import "./ToDoOverviewBody.css"

export default function ToDoOverviewBody() {
  return (
    <div>
      <h2>Subject</h2>
      <button>+</button>
      <div className="status-frame">
        <h3>Description: Kündigung von Herrn Ammann</h3>
        <h4>Due Date: 10.03.2025</h4>
        <h5>Bearbeiter: Macel Barth</h5>  
        <h6>Status: Erledigt</h6>
      </div>
      <div className="Task2">
        <h3>Description: Desing der Website erstellen</h3>
        <h4>Due Date: 10.03.2025</h4>
        <h5>Bearbeiter: Finn Becher</h5>  
        <h6>Status: In Bearbeitung</h6>
      </div>
    </div>
  );
 
}

