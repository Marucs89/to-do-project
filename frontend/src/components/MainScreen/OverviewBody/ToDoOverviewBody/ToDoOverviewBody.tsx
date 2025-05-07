import "./ToDoOverviewBody.css";
import { ToDos } from "../../../../schemas/to-do";
import { addDays, format, nextSunday, previousMonday } from "date-fns";
import _ from "lodash";
import { createMarkerForTask } from "./helper";
import Modal from "./Modal";
import { useEffect } from "react";

export default function ToDoOverviewBody({
  toDos,
}: {
  toDos: ToDos | undefined;
}) {
  useEffect(() => {
    const buttons = document.querySelectorAll(".tabBtn");
    console.log("ccc", buttons);
    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        buttons.forEach((btn) => btn.classList.remove("active"));
        button.classList.add("active");
      });
    });
  }, []);

  const now = new Date();
  let monday;
  if (now.getUTCDay() === 1) {
    monday = now;
  } else {
    monday = previousMonday(now);
  }

  const createThisWeekTableHeader = () => {
    const sunday = nextSunday(new Date());
    let currentDate = monday;
    const tableHeaders = [];
    while (currentDate <= sunday) {
      tableHeaders.push(
        <th style={{ padding: "3px", paddingLeft: "16px" }}>
          <p style={{ alignContent: "center" }}>
            {`${format(currentDate, "EE")} (${format(currentDate, "dd/MM")})`}
          </p>
        </th>
      );
      currentDate = addDays(currentDate, 1);
    }
    return tableHeaders;
  };

  const createThisWeekTableBody = (toDos: ToDos | undefined) => {
    const sunday = nextSunday(new Date());
    let currentDate = monday;
    const tableBodys = [];
    while (currentDate <= sunday) {
      let i = 0;
      const currentMonthYear = format(currentDate, "dd/MM/yy");
      const currentToDos = _.filter(toDos, (toDo) => {
        return (
          format(new Date(toDo?.deadline ?? 0), "dd/MM/yy") === currentMonthYear
        );
      });
      tableBodys.push(
        <td
          style={{
            padding: "0px",
            marginTop: "2px",
          }}
        >
          {currentToDos.length > 0 &&
            currentToDos.map((toDo) => {
              const paddingTop = i === 0 ? "0px" : "16px";
              i++;
              return (
                <div>
                  <div
                    className='uk-grid  cell-div'
                    style={{
                      background: createMarkerForTask(toDo.arbeiter),
                      marginTop: paddingTop,
                      padding: "4px",
                      borderRadius: "4px",
                      marginLeft: "5px",
                    }}
                    onClick={() =>
                      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
                      //@ts-ignore
                      document.getElementById(`${toDo.todo_id}`)?.showModal()
                    }
                    uk-grid
                  >
                    <p style={{ paddingLeft: "12px" }}>{toDo.name}</p>
                  </div>
                  <Modal toDo={toDo} />
                </div>
              );
            })}
        </td>
      );
      currentDate = addDays(currentDate, 1);
    }
    console.log("Tablebodys: ", tableBodys);
    return tableBodys;
  };

  return (
    <div>
      <div>
        <table
          className='uk-table uk-margin-top uk-margin-right'
          style={{
            borderCollapse: "separate",
            borderSpacing: "40px",
          }}
        >
          <thead>
            <tr>{createThisWeekTableHeader()}</tr>
          </thead>
          <tbody>
            <tr>{createThisWeekTableBody(toDos)}</tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
