import {
  addDays,
  format,
  nextMonday,
  nextSunday,
  previousMonday,
} from "date-fns";
import useEmblaCarousel from "embla-carousel-react";
import _ from "lodash";
import { useCallback, useEffect, useState } from "react";
import { AllAssignees } from "../../../../schemas/assignees";
import { ToDos } from "../../../../schemas/to-do";
import { AllTopics } from "../../../../schemas/topics";
import { createMarkerForTask } from "./helper";
import Modal from "./Modal";
import "./ToDoOverviewBody.css";

export default function ToDoOverviewBody({
  toDos,
  allTopics,
  allAssignees,
}: {
  toDos: ToDos | undefined;
  allTopics: AllTopics | undefined;
  allAssignees: AllAssignees | undefined;
}) {
  const [emblaRef, emblaApi] = useEmblaCarousel({ loop: false });

  const scrollPrev = useCallback(
    () => emblaApi && emblaApi.scrollPrev(),
    [emblaApi]
  );
  const scrollNext = useCallback(
    () => emblaApi && emblaApi.scrollNext(),
    [emblaApi]
  );

  const [prevBtnEnabled, setPrevBtnEnabled] = useState(false);
  const [nextBtnEnabled, setNextBtnEnabled] = useState(false);
  let count = 0;
  let weekTableSlides = [];
  const onSelect = useCallback(() => {
    if (!emblaApi) return;
    setPrevBtnEnabled(emblaApi.canScrollPrev());
    setNextBtnEnabled(emblaApi.canScrollNext());
  }, [emblaApi]);

  useEffect(() => {
    if (!emblaApi) return;
    onSelect();
    emblaApi.on("select", onSelect);
  }, [emblaApi, onSelect]);

  useEffect(() => {}, []);
  const now = new Date();
  let currentMonday;
  if (now.getUTCDay() === 1) {
    currentMonday = now;
  } else {
    currentMonday = previousMonday(now);
  }

  const createWeekTableHeader = (start: Date) => {
    const sunday = nextSunday(start);
    let currentDate = start;
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

  const createWeekTableBody = (toDos: ToDos | undefined, start: Date) => {
    const sunday = nextSunday(start);
    let currentDate = start;
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
                    className='uk-grid cell-div'
                    style={{
                      background: createMarkerForTask(toDo.arbeiter),
                      marginTop: paddingTop,
                      padding: "4px",
                      borderRadius: "4px",
                      marginLeft: "5px",
                    }}
                    onClick={() => {
                      const modalDialog = document.getElementById(
                        `modal-${toDo.todo_id}`
                      ) as HTMLDialogElement;
                      modalDialog.showModal();
                    }}
                    uk-grid='true'
                  >
                    <p style={{ paddingLeft: "12px" }}>{toDo.name}</p>
                  </div>
                  <Modal
                    toDo={toDo}
                    allTopics={allTopics}
                    allAssignees={allAssignees}
                  />
                </div>
              );
            })}
        </td>
      );
      currentDate = addDays(currentDate, 1);
    }
    return tableBodys;
  };

  const createToDosTable = (start: Date) => {
    let monday = previousMonday(start);
    if (start.getUTCDay() === 1) {
      monday = start;
    }
    const mondayAfter = nextMonday(monday);
    const nextMondayAfter = nextMonday(mondayAfter);
    weekTableSlides.push(
      <div className='embla__slide'>
        <table
          style={{
            borderSpacing: "40px",
          }}
        >
          <thead>
            <tr>{createWeekTableHeader(monday)}</tr>
          </thead>
          <tbody>
            <tr>{createWeekTableBody(toDos, monday)}</tr>
          </tbody>
        </table>
        <table
          style={{
            borderSpacing: "40px",
          }}
        >
          <thead>
            <tr>{createWeekTableHeader(mondayAfter)}</tr>
          </thead>
          <tbody>
            <tr>{createWeekTableBody(toDos, mondayAfter)}</tr>
          </tbody>
        </table>
      </div>
    );

    if (count === 1) {
      return;
    } else {
      count++;
      createToDosTable(nextMondayAfter);
    }
  };

  createToDosTable(currentMonday);
  console.log("test: ", weekTableSlides);
  return (
    <div className='tableContainer embla' ref={emblaRef}>
      <div className='embla__container'>
        {weekTableSlides.map((test) => {
          return test;
        })}
      </div>
      <div id='sliderButtonsDiv'>
        <button
          className='sliderButtons'
          style={{ position: "absolute", left: 0 }}
          onClick={scrollPrev}
          disabled={!prevBtnEnabled}
        >
          {"<"}
        </button>
        <button
          className='sliderButtons'
          style={{ position: "absolute", right: 0 }}
          onClick={scrollNext}
          disabled={!nextBtnEnabled}
        >
          {">"}
        </button>
      </div>
    </div>
  );
}
