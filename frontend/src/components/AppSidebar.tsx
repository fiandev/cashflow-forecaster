import { 
  LayoutDashboard, 
  Receipt, 
  Settings, 
  TrendingUp,
  User
} from "lucide-react";
import { NavLink } from "react-router-dom";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";

const navigationItems = [
  {
    title: "Dashboard",
    icon: LayoutDashboard,
    to: "/",
  },
  {
    title: "Add Transaction",
    icon: Receipt,
    to: "/transactions",
  },
  {
    title: "Business Setup",
    icon: Settings,
    to: "/business-setup",
  },
  {
    title: "Forecast Input",
    icon: TrendingUp,
    to: "/forecast",
  },
];

export const AppSidebar = () => {
  return (
    <Sidebar>
      <SidebarHeader>
        <div className="px-2 py-1">
          <h2 className="text-lg font-semibold text-sidebar-foreground">
            AI Cashflow
          </h2>
          <p className="text-xs text-muted-foreground">
            Risk Analyst
          </p>
        </div>
      </SidebarHeader>
      
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {navigationItems.map((item) => (
                <SidebarMenuItem key={item.to}>
                  <SidebarMenuButton asChild>
                    <NavLink
                      to={item.to}
                      className={({ isActive }) =>
                        isActive ? "bg-sidebar-accent text-sidebar-accent-foreground" : ""
                      }
                    >
                      <item.icon className="h-4 w-4" />
                      <span>{item.title}</span>
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton>
              <User className="h-4 w-4" />
              <span>Profile</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
};