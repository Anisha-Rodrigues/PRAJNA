import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute() {
  const { officer } = useAuth();
  const location = useLocation();

  if (!officer) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return <Outlet />;
}
