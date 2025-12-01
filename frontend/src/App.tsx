import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import { Header } from "@/components/Header";
import { AuthInitializer } from "@/components/AuthInitializer";
import ProtectedRoute from "@/components/ProtectedRoute";
import { BusinessProvider } from "@/contexts/BusinessContext";
import Index from "./pages/Index";
import Transactions from "./pages/Transactions";
import BusinessSetup from "./pages/BusinessSetup";
import NewBusiness from "./pages/NewBusiness";
import Forecast from "./pages/Forecast";
import ForecastResults from "./pages/ForecastResults";
import Profile from "./pages/Profile";
import Login from "./pages/Login";
import Register from "./pages/Register";
import RegisterBusiness from "./pages/RegisterBusiness";
import ResetPassword from "./pages/ResetPassword";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <BusinessProvider>
          <SidebarProvider>
            <AuthInitializer />
            <AppSidebar />
            <SidebarInset>
              <Header />
              <Routes>
                {/* Auth Routes */}
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/register-business" element={<RegisterBusiness />} />
                <Route path="/reset-password" element={<ResetPassword />} />

                {/* Protected Routes */}
                <Route path="/" element={
                  <ProtectedRoute>
                    <Index />
                  </ProtectedRoute>
                } />
                <Route path="/transactions" element={
                  <ProtectedRoute>
                    <Transactions />
                  </ProtectedRoute>
                } />
                <Route path="/business-setup" element={
                  <ProtectedRoute>
                    <BusinessSetup />
                  </ProtectedRoute>
                } />
                <Route path="/business/new" element={
                  <ProtectedRoute>
                    <NewBusiness />
                  </ProtectedRoute>
                } />
                <Route path="/forecast" element={
                  <ProtectedRoute>
                    <Forecast />
                  </ProtectedRoute>
                } />
                <Route path="/forecast/results" element={
                  <ProtectedRoute>
                    <ForecastResults />
                  </ProtectedRoute>
                } />
                <Route path="/profile" element={
                  <ProtectedRoute>
                    <Profile />
                  </ProtectedRoute>
                } />

                {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
                <Route path="*" element={<NotFound />} />
              </Routes>
            </SidebarInset>
          </SidebarProvider>
        </BusinessProvider>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
