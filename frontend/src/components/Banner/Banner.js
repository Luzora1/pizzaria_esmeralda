import React from "react";
import "./Banner.css";
import Button from "../Button/Button";

const Banner = () => {
  return (
    <div className="banner">
      <div className="banner__body">
        <h2>Crafite sua pizza!</h2>
        <p>
          Que tal inventar sua própia pizza?<br></br> Escolha dentre uma
          variedade de ingredientes e crafite sua pizza única!
        </p>
        <Button text="CRAFTAR!" color="#367723" />
      </div>
    </div>
  );
};

export default Banner;
