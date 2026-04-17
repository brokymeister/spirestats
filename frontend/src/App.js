import { useEffect, useState } from "react";
import Overview from "./components/Overview";
import Cards from "./components/Cards";
import Relics from "./components/Relics";
import Encounters from "./components/Encounters";

function App() {
  const [overview, setOverview] = useState(null);
  const [cards, setCards] = useState(null);
  const [tab, setTab] = useState("overview")
  const [relics, setRelics] = useState(null);
  const [encounters, setEncounters] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/overview")
      .then((res) => res.json())
      .then((data) => setOverview(data));

    fetch("http://127.0.0.1:8000/api/cards")
      .then((res) => res.json())
      .then((data) => setCards(data));

    fetch("http://127.0.0.1:8000/api/relics")
      .then(res => res.json())
      .then((data) => setRelics(data));

    fetch("http://127.0.0.1:8000/api/encounters")
      .then(res => res.json())
      .then((data) => setEncounters(data));
  }, []);

  if (!overview || !cards || !encounters || !relics) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ marginBottom: "20px" }}>
      <button onClick={() => setTab("overview")}>Overview</button>
      <button onClick={() => setTab("cards")}>Cards</button>
      <button onClick={() => setTab("relics")}>Relics</button>
      <button onClick={() => setTab("encounters")}>Encounters</button>

      {tab === "overview" && <Overview overview={overview} />}

      {tab === "cards" && <Cards cards={cards} />}

      {tab === "relics" && <Relics relics={relics} />}

      {tab === "encounters" && <Encounters encounters={encounters} />}
    </div>
  );
}

export default App;