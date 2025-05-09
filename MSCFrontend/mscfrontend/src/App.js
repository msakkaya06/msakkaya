import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ProfilePage from "./pages/ProfilePage";
import DashboardPage from "./pages/DashboardPage";
import PrivateRoute from "./components/PrivateRoute"; // en üste
import Navbar from "./components/Navbar"; // en üste ekle

function App() {
  return (
    <Router>
      <Navbar /> {/* burada */}
      <Routes>
        <Route path="/" element={<div className="text-center mt-10">Ana Sayfa</div>} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <DashboardPage />
            </PrivateRoute>
          }
        />
        <Route
          path="/me"
          element={
            <PrivateRoute>
              <ProfilePage />
            </PrivateRoute>
          }
        />
        <Route
          path="/admin-area"
          element={
            <PrivateRoute>
              <div className="p-8">Yönetim Paneli (placeholder)</div>
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
