import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import { Header } from "@/components/Header";
import Index from "./pages/Index";
import Transactions from "./pages/Transactions";
import BusinessSetup from "./pages/BusinessSetup";
import Forecast from "./pages/Forecast";
import ForecastResults from "./pages/ForecastResults";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <SidebarProvider>
          <AppSidebar />
          <SidebarInset>
            <Header />
            <Routes>
              <Route path="/" element={<Index />} />
              <Route path="/transactions" element={<Transactions />} />
              <Route path="/business-setup" element={<BusinessSetup />} />
              <Route path="/forecast" element={<Forecast />} />
              <Route path="/forecast/results" element={<ForecastResults />} />
              {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
              <Route path="*" element={<NotFound />} />
            </Routes>
          </SidebarInset>
        </SidebarProvider>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
