import { Header } from "./pages/Header";
import { Route, Routes, Link } from 'react-router-dom';
import { Home } from "./pages/Home"
import { Guide } from "./pages/Guide";
import { Bot } from "./pages/BotPage";
import { Statistics } from "./pages/StatisticsPage";

function App() {
  return (
    <div>
      <Header />
      <div className="App">
        <Routes>
          <Route path='/' element={<Home></Home>}></Route>
          <Route path='/guide' element={<Guide></Guide>}></Route>
          <Route path='/bot' element={<Bot></Bot>}></Route>
          <Route path='/Statistics' element={<Statistics></Statistics>}></Route>
        </Routes >
      </div>
    </div>
  );
}

export default App;
