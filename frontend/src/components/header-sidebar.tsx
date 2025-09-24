"use client";
import { PanelLeftClose, PanelRightClose } from "lucide-react";
import { SidebarMenuButton, useSidebar } from "./ui/sidebar";

export default function HeaderSidebar() {
  const { toggleSidebar, open } = useSidebar();
  return (
    <SidebarMenuButton asChild>
      <a href="#" onClick={toggleSidebar}>
        {open ? <PanelLeftClose /> : <PanelRightClose />}
        <span>Home</span>
      </a>
    </SidebarMenuButton>
  );
}
