import React from "react";
import "./Cta.css";
import Button from "../Button/Button";

const Cta = () => {
  return (
    <div className="cta">
      <div className="cta__img">
        <div className="cta__img__text">
          <h2>Crafite sua pizza única!</h2>
          <Button text="Craftar!" />
        </div>
      </div>
    </div>
  );
};

export default Cta;
