import { SidebarTrigger } from "@/components/ui/sidebar";
import UserProfileCard from "@/components/UserProfileCard";

export const Header = () => {
  return (
    <header className="border-b border-border bg-card sticky top-0 z-50">
      <div className="flex items-center gap-4 px-4 py-4">
        <SidebarTrigger />
        
        <div className="flex-1">
          <h1 className="text-xl font-bold">AI Cashflow & Risk Analyst</h1>
          <p className="text-xs text-muted-foreground">MVP Dashboard</p>
        </div>

        <div className="flex items-center gap-3">
          <UserProfileCard />
        </div>
      </div>
    </header>
  );
};
