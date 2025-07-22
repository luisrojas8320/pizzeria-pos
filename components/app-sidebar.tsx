"use client"

import {
  BarChart3,
  ChefHat,
  ClipboardList,
  Home,
  Package,
  PizzaIcon,
  ShoppingCart,
  TrendingUp,
  Users,
  UserCheck,
} from "lucide-react"
import Link from "next/link"
import { usePathname } from "next/navigation"

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

const menuItems = [
  {
    title: "Dashboard",
    url: "/",
    icon: Home,
  },
  {
    title: "Pedidos",
    url: "/orders",
    icon: ClipboardList,
  },
  {
    title: "Compras",
    url: "/purchases",
    icon: ShoppingCart,
  },
  {
    title: "Personal",
    url: "/staff",
    icon: Users,
  },
  {
    title: "Menú",
    url: "/menu",
    icon: ChefHat,
  },
  {
    title: "Reportes",
    url: "/reports",
    icon: BarChart3,
  },
  {
    title: "Clientes",
    url: "/customers",
    icon: UserCheck,
  },
  {
    title: "Inventario",
    url: "/inventory",
    icon: Package,
  },
  {
    title: "Análisis",
    url: "/analytics",
    icon: TrendingUp,
  },
]

export function AppSidebar() {
  const pathname = usePathname()

  return (
    <Sidebar className="border-r">
      <SidebarHeader className="border-b p-4">
        <div className="flex items-center gap-2 min-w-0">
          <PizzaIcon className="h-8 w-8 text-orange-500 flex-shrink-0" />
          <div className="min-w-0 flex-1">
            <h2 className="text-lg font-semibold truncate">Delizzia POS</h2>
            <p className="text-sm text-muted-foreground truncate">Pizzería Ibarra</p>
          </div>
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Gestión</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {menuItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild isActive={pathname === item.url}>
                    <Link href={item.url} className="flex items-center gap-3 min-w-0">
                      <item.icon className="flex-shrink-0" />
                      <span className="truncate">{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}
