import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import DashboardLayout from "./pages/DashboardLayout";
import HomePage from "./pages/HomePage";
import ChatCanvasPage from "./pages/ChatCanvasPage";
import PressureMapPage from "./pages/PressureMapPage";
import ProfilePage from "./pages/ProfilePage";

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/app" element={<DashboardLayout />}>
            <Route index element={<HomePage />} />
            <Route path="chat" element={<ChatCanvasPage />} />
            <Route path="pressure" element={<PressureMapPage />} />
            <Route path="profile" element={<ProfilePage />} />
          </Route>
        </Route>

        <Route path="*" element={<Navigate to="/app" replace />} />
      </Routes>
    </AuthProvider>
  );
}
