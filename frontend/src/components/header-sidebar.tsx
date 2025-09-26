// "use client";
import { PanelLeftClose, PanelRightClose } from "lucide-react";
import { SidebarMenuButton, useSidebar } from "./ui/sidebar";
import Link from "next/link";
import { ModeToggle } from "./ui/mode-toggle";
export default function HeaderSidebar() {
  const { toggleSidebar, open } = useSidebar();
  return (
    <SidebarMenuButton asChild>
      <Link
        href={"#"}
        onClick={toggleSidebar}
        className="w-full justify-start p-3 h-12"
      >
        {open ? (
          <PanelLeftClose className="mr-3 w-12 h-12" />
        ) : (
          <PanelRightClose className="mr-3 w-12 h-12" />
        )}
        <div className="flex flex-col items-start">
          <div className="font-semibold">English Hub</div>
          <div className="text-xs text-muted-foreground">
            Learn smarter, faster
          </div>
        </div>
      </Link>
    </SidebarMenuButton>
  );
}
