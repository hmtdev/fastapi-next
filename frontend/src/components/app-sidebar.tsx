"use client";
import { useState } from "react";
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
  SidebarSeparator,
} from "@/components/ui/sidebar";
import {
  BookOpen,
  Users,
  BarChart3,
  Brain,
  Trophy,
  Zap,
  Tv,
} from "lucide-react";
import HeaderSidebar from "./header-sidebar";
import { NavUser } from "./nav-user";
import Link from "next/link";

// Menu items
const items = [
  {
    id: "Dashboard",
    url: "/dashboard",
    icon: BarChart3,
    description: "Overview & Progress",
  },
  {
    id: "Courses",
    url: "/dashboard/users",
    icon: BookOpen,
    description: "Learning Path",
  },
  {
    id: "Flashcards",
    url: "/dashboard/flashcards",
    icon: Brain,
    description: "Memory Training",
  },
  {
    id: "Shadowing",
    url: "/dashboard/shadow",
    icon: Tv,
    description: "Youtube Practice",
  },
  {
    id: "Practice",
    url: "/dashboard/shadow",
    icon: Zap,
    description: "Interactive Tools",
  },
  {
    id: "Community",
    url: "/dashboard/shadow",
    icon: Users,
    description: "Connect & Share",
  },
  {
    id: "Archivements",
    url: "/dashboard/shadow",
    icon: Trophy,
    description: "Goals & Rewards",
  },
];
export default function AppSidebar({
  ...props
}: React.ComponentProps<typeof Sidebar>) {
  const [activeItem, setActiveItem] = useState<string | null>(items[0].id);

  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <HeaderSidebar />
      </SidebarHeader>
      <SidebarSeparator />
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu className="gap-1">
              {items.map((item) => (
                <SidebarMenuItem key={item.id}>
                  <SidebarMenuButton
                    asChild
                    className={
                      activeItem === item.id
                        ? "bg-primary text-primary-foreground"
                        : ""
                    }
                    isActive={activeItem === item.id}
                    onClick={() => setActiveItem(item.id)}
                  >
                    <Link
                      href={item.url}
                      className="w-full justify-start p-3 h-12"
                    >
                      <item.icon className="mr-3 w-12 h-12" />
                      <div className="flex flex-col items-start">
                        <div className="font-semibold">{item.id}</div>
                        <div className="text-xs text-muted-foreground">
                          {item.description}
                        </div>
                      </div>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter>{<NavUser />}</SidebarFooter>
    </Sidebar>
  );
}
