import { SidebarTrigger } from "@/components/ui/sidebar";
import UserProfileCard from "@/components/UserProfileCard";
import BusinessSelector from "@/components/BusinessSelector";
import { Link } from "react-router-dom";

export const Header = () => {
  return (
    <header className="fixed top-0 z-50 w-full border-b border-border bg-card">
      <div className="flex items-center gap-4 px-4 py-4">
        <SidebarTrigger />

        <div className="flex-1 min-w-0">
          <h1 className="text-xl font-bold truncate">
            <Link to="/" rel="noopener noreferrer">
              AI Cashflow & Risk Analyst
            </Link>
          </h1>
          <p className="text-xs text-muted-foreground hidden sm:block">MVP Dashboard</p>
        </div>

        <div className="flex items-center gap-2 md:gap-3">
          <div className="w-40 sm:w-48 md:w-52">
            <BusinessSelector />
          </div>
          <UserProfileCard />
        </div>
      </div>
    </header>
  );
};
