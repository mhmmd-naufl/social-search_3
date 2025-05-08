import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import Hasil from './Hasil';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/hasil" element={<Hasil />} />
      </Routes>
    </Router>
  );
}

export default App;
