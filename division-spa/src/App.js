import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Footer from './components/Footer';
import HomePage from './pages/HomePage/HomePage';

function App() {
  return (
    <Router>
    <main class="flex-shrink-0">
      <Routes>
      <Route path='/' component={HomePage} exact />
      </Routes>
      <span>
        Boobies
      </span>
    </main>
    <Footer />
    </Router>
  );
}

export default App;
