import Header from "./components/Header/Header";
import Cta from "./components/Cta/Cta";
import About from "./components/About/About";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  return (
    <div className="App">
      <Header />
      <Cta />
      <About />
    </div>
  );
}

export default App;
