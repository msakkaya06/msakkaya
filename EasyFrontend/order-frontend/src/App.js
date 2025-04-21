import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginRedirect from "./pages/LoginRedirect";
import LogoutPage from "./pages/LogoutPage";
import Cart from "./pages/Cart";
import Home from "./pages/Home"; // Ürünleri gösterdiğin sayfa

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login-redirect" element={<LoginRedirect />} />
        <Route path="/" element={<Home />} />
        <Route path="/logout" element={<LogoutPage />} />
        <Route path="/cart" element={<Cart />} />
      </Routes>
    </Router>
  );
}

export default App;
