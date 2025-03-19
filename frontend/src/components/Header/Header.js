import React from "react";
import Button from "../Button/Button";
import "./Header.css";
const Header = () => {
  return (
    <div className="header">
      <div className="header__logg">
        <h1>P . E</h1>
      </div>
      <div className="header__menu">
        <div className="header__menu__buttons">
          <Button text={"Pizzas"} />
          <Button text={"Contato"} />
          <Button text={"Sobre Nós"} />
        </div>

        <div className="header__menu__user">
          <div className="header__menu__user__icons">
            <p>user</p>
            <p>Carrinho</p>
          </div>
          <div className="header__menu__user__info">
            <p>Esmeraldas = 68</p>
            <p>Level = 12</p>
          </div>
          <div className="header__menu__user__xpBar">
            <div
              className="header__menu__user__info__xpBarProgression"
              style={{
                backgroundColor: "rgb(88, 185, 24)",
                width: "64%",
                height: "4px",
              }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header;
