import { SidebarTrigger } from "@/components/ui/sidebar";
import UserProfileCard from "@/components/UserProfileCard";
import BusinessSelector from "@/components/BusinessSelector";
import { Link } from "react-router-dom";
import { useAuthStore } from "@/stores/auth-store";

export const Header = () => {
  const { isAuthenticated } = useAuthStore();

  return (
    <header className="fixed lg:sticky top-0 z-50 w-full border-b border-border bg-card">
      <div className="flex items-center gap-4 px-4 py-4">
        <SidebarTrigger />

        <div className="flex-1 min-w-0">
          <h1 className="text-xl font-bold truncate">
            <Link to="/" rel="noopener noreferrer">
              Cashflow Forecaster
            </Link>
          </h1>
          <p className="text-xs text-muted-foreground hidden sm:block">
            AI Powered Cashflow Forecaster
          </p>
        </div>

        {isAuthenticated && (
          <div className="flex items-center gap-2 md:gap-3">
            <div className="w-40 sm:w-48 md:w-52">
              <BusinessSelector />
            </div>
            <UserProfileCard />
          </div>
        )}
      </div>
    </header>
  );
};
