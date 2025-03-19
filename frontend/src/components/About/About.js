import React from "react";
import "./About.css";

const About = () => {
  return (
    <div className="about">
      <h2>Quem Somos</h2>
      <div className="about__cards">
        <div className="about__card">
          <div className="about__card__text">
            <h3>Criando o mundo</h3>
            <p>
              Tudo começou em uma pequena mesa de crafting, onde ideias e sonhos
              se transformaram em algo maior. A Pizzaria Esmeralda nasceu da
              paixão por dois universos: o mundo infinito de Minecraft e a arte
              de fazer pizzas. Nós, os fundadores, éramos um grupo de amigos que
              passava horas explorando cavernas, construindo castelos e, claro,
              discutindo qual seria o sabor perfeito de pizza para acompanhar
              essas aventuras. Um dia, durante uma maratona de Minecraft, surgiu
              a pergunta: "E se pudéssemos trazer a magia do jogo para o mundo
              real?" Foi assim que decidimos criar uma pizzaria temática, onde
              cada pizza fosse uma homenagem aos biomas, criaturas e blocos que
              tanto amamos. Começamos com um pequeno forno a lenha e muitas
              ideias pixeladas, e hoje estamos aqui, prontos para compartilhar
              essa aventura com você!
            </p>
          </div>
        </div>
        <div className="about__card">
          <div className="about__card__text">
            <h3>Nossa missão</h3>
            <p>
              Na Craft & Slice, nossa missão é simples: unir pessoas através de
              pizzas e aventuras. Queremos ser mais do que uma pizzaria;
              queremos ser um lugar onde jogadores, famílias e amigos possam se
              reunir para celebrar a criatividade, a diversão e, claro, o sabor.
              Inspirados pelo espírito de exploração e colaboração de Minecraft,
              buscamos sempre inovar, trazendo sabores únicos e experiências
              memoráveis. Cada pizza que criamos é feita com ingredientes de
              alta qualidade, preparada com carinho e entregue com um toque de
              magia pixelada. Além disso, estamos comprometidos em construir um
              mundo melhor – assim como no jogo, onde cada bloco colocado faz a
              diferença. Por isso, apoiamos práticas sustentáveis e trabalhamos
              com fornecedores locais, garantindo que cada pedaço de pizza seja
              uma escolha que faz bem para você e para o planeta. Junte-se a nós
              nessa jornada! Aqui, todo dia é uma nova aventura, e cada pizza é
              uma obra-prima craftada especialmente para você.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
