import React from "react";
import "./Button.css";

const Button = ({ text, goTo, color }) => {
  return (
    <div className="button" style={{ backgroundColor: color }}>
      {text}
    </div>
  );
};

export default Button;
