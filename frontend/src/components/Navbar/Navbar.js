import React from "react";
import "./Navbar.css";
import Button from "../Button/Button";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser } from "@fortawesome/free-solid-svg-icons";
import { faCartShopping } from "@fortawesome/free-solid-svg-icons";

const Navbar = () => {
  return (
    <div className="navbar">
      <h2>Pizzaria Esmeralda</h2>
      <div className="navbar__menu">
        <Button text="Pizzas & bebidas" color="#367723" />
        <Button text="Sobre nós" color="#99918e" />
        <Button text="Contato" color="#99918e" />
      </div>
      <div className="navbar__actions">
        <div className="navbar__icons">
          <FontAwesomeIcon icon={faCartShopping} />
          <div className="user">
            <FontAwesomeIcon icon={faUser} />
            <p>nome</p>
          </div>
        </div>
        <div className="navbar__xp">
          <p>LV 28</p>
          <div className="navbar__xp__bar">
            <div
              className="navbar__xp__bar__progresssion"
              style={{
                width: "47%",
              }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Navbar;
