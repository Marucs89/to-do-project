import { StylesConfig } from "react-select";
import makeAnimated from "react-select/animated";
export const animatedComponent = makeAnimated();

export const assigneesSelectStyles: StylesConfig<
  { value: number; label: string }[]
> = {
  control: (styles) => {
    return {
      ...styles,
      width: "250px",
      ":hover": { cursor: "pointer" },
    };
  },
  option: (styles) => {
    return {
      ...styles,
      color: "black",
      cursor: "pointer",
      justifySelf: "center",
    };
  },
};

export const topicsSelectStyles: StylesConfig<
  { value: number; label: string }[]
> = {
  control: (styles) => {
    return { ...styles, width: "11rem", ":hover": { cursor: "pointer" } };
  },
  option: (styles) => {
    return {
      ...styles,
      color: "black",
      cursor: "pointer",
      justifySelf: "center",
    };
  },
};
