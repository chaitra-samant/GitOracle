
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import LandingPage from './pages/LandingPage';
import MainPage from './pages/MainPage';

function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/app" element={<MainPage />} />
      </Routes>
    </div>
  );
}

export default App;