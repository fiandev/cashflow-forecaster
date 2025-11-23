import { User } from "lucide-react";
import { SidebarTrigger } from "@/components/ui/sidebar";

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
          <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
            <User className="w-4 h-4 text-primary" />
          </div>
        </div>
      </div>
    </header>
  );
};
