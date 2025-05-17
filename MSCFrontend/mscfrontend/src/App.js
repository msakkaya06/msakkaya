import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ProfilePage from "./pages/ProfilePage";
import CloudPage from "./pages/CloudPage";
import DashboardPage from "./pages/DashboardPage";

import PrivateRoute from "./components/PrivateRoute";
import Navbar from "./components/Navbar";
import AdminAreaPage from "./pages/AdminAreaPage";
import { ToastProvider } from "./context/ToastContext"; // 🔥 bunu ekle
import { ModalProvider } from "./context/ModalContext";

function App() {
  return (
    <ToastProvider> {/* 🔥 En dış katman */}
      <ModalProvider>
        <Router>
          <Navbar />
          <Routes>
            <Route path="/" element={<LoginPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/cloud/:folderId?" 
              element={
                <PrivateRoute>
                  <CloudPage  />
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
                  <AdminAreaPage />
                </PrivateRoute>
              }
            />
          </Routes>
        </Router>
      </ModalProvider>
    </ToastProvider>
  );
}

export default App;
