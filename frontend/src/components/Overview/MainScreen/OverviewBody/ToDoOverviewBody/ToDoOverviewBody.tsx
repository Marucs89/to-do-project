import "./ToDoOverviewBody.css";
import { ToDos } from "../../../../../schemas/to-do";
import { addDays, format, nextSunday, previousMonday } from "date-fns";
import _ from "lodash";

export default function ToDoOverviewBody({
  toDos,
}: {
  toDos: ToDos | undefined;
}) {
  console.log("date of ToDo: ", toDos ? toDos[0].deadline : null);
  // const dueDate = deadline
  //   ? format(new Date(deadline), "dd.MM.yyyy")
  //   : "no due Date!";

  // const bearbeiter = arbeiter
  //   ? `${arbeiter[0].name} ${arbeiter[0].lastname}`
  //   : "no Bearbeiter";
  // const stage = status?.name;
  const monday = previousMonday(new Date());
  // console.log("Date now: ", new Date());
  // console.log("Monday: ", monday);
  const createThisWeekTableHeader = () => {
    const sunday = nextSunday(new Date());
    let currentDate = monday;
    const tableHeaders = [];
    while (currentDate < sunday) {
      tableHeaders.push(
        <th style={{ padding: "3px" }}>
          <p>
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
    while (currentDate < sunday) {
      const currentMonthYear = format(currentDate, "MM/yy");
      const currentToDos = _.filter(toDos, (toDo) => {
        return (
          format(new Date(toDo?.deadline ?? 0), "MM/yy") === currentMonthYear
        );
      });
      tableBodys.push(
        <td style={{ padding: "3px" }}>
          {currentToDos.length > 0 ? (
            currentToDos.map((toDo) => {
              return <p style={{ paddingRight: "30px" }}>{toDo.name}</p>;
            })
          ) : (
            <>
              <p style={{ paddingRight: "30px" }}>Empty</p>
            </>
          )}
        </td>
      );
      currentDate = addDays(currentDate, 1);
    }
    return tableBodys;
  };

  return (
    <div className=''>
      <table
        className='uk-table'
        style={{ borderCollapse: "separate", borderSpacing: "20px" }}
      >
        <thead>
          <tr>{createThisWeekTableHeader()}</tr>
        </thead>
        <tbody>
          <tr>{createThisWeekTableBody(toDos)}</tr>
        </tbody>
      </table>
    </div>
  );
}
