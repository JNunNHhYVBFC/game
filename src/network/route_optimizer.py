import subprocess
import platform
from typing import List, Dict
import json
import os

class RouteOptimizer:
    def __init__(self):
        self.platform = platform.system().lower()
        self.current_routes = []
        
    def get_current_routes(self) -> List[Dict]:
        """
        Получает текущую таблицу маршрутизации
        """
        routes = []
        try:
            if self.platform == "windows":
                output = subprocess.check_output(["route", "print"], universal_newlines=True)
                # Парсим вывод Windows route
                lines = output.split("\n")
                active_section = False
                for line in lines:
                    if "Active Routes:" in line:
                        active_section = True
                        continue
                    if active_section and line.strip():
                        parts = line.split()
                        if len(parts) >= 4:
                            routes.append({
                                "network": parts[0],
                                "netmask": parts[1],
                                "gateway": parts[2],
                                "interface": parts[3]
                            })
            else:
                # Для Linux используем ip route
                output = subprocess.check_output(["ip", "route"], universal_newlines=True)
                for line in output.split("\n"):
                    if line.strip():
                        routes.append({"route": line.strip()})
                        
        except subprocess.CalledProcessError:
            pass
            
        self.current_routes = routes
        return routes
        
    def optimize_route(self, target_ip: str, preferred_gateway: str = None) -> bool:
        """
        Оптимизирует маршрут до целевого IP
        """
        try:
            if self.platform == "windows":
                # Добавляем статический маршрут через предпочтительный шлюз
                if preferred_gateway:
                    cmd = ["route", "add", target_ip, "mask", "255.255.255.255", preferred_gateway]
                    subprocess.check_call(cmd)
                    return True
            else:
                if preferred_gateway:
                    cmd = ["ip", "route", "add", target_ip, "via", preferred_gateway]
                    subprocess.check_call(cmd)
                    return True
                    
        except subprocess.CalledProcessError:
            return False
            
        return False
        
    def reset_routes(self):
        """
        Сбрасывает оптимизированные маршруты
        """
        try:
            if self.platform == "windows":
                # Сброс всех статических маршрутов
                subprocess.check_call(["route", "flush"])
            else:
                # Для Linux перезагружаем сетевой сервис
                subprocess.check_call(["systemctl", "restart", "networking"])
                
        except subprocess.CalledProcessError:
            pass
