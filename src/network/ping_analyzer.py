import subprocess
import platform
import re
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class PingAnalyzer:
    def __init__(self):
        self.platform = platform.system().lower()
    
    def ping(self, host: str, count: int = 4) -> Tuple[float, float, float]:
        """
        Выполняет пинг до указанного хоста и возвращает статистику
        Returns: (min_ping, avg_ping, max_ping)
        """
        try:
            if self.platform == "windows":
                # На Windows добавляем параметр -w для таймаута (в миллисекундах)
                cmd = ["ping", "-n", str(count), host]
                # Используем специальную кодировку для Windows
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=startupinfo,
                    universal_newlines=False
                )
                output, error = process.communicate()
                
                # Декодируем вывод с использованием cp866 (кодировка командной строки Windows)
                output = output.decode('cp866')
                logger.debug(f"Raw ping output: {output}")
                
                # Ищем строку со средним временем
                avg_match = re.search(r"среднее\s*=\s*(\d+)\s*мсек", output.lower())
                if avg_match:
                    avg_time = float(avg_match.group(1))
                    return avg_time, avg_time, avg_time
                
                # Если не нашли среднее, ищем отдельные значения времени
                times = re.findall(r"время=(\d+)мс", output.lower())
                if times:
                    times = [float(t) for t in times]
                    return min(times), sum(times)/len(times), max(times)
                
                # Если ничего не нашли, возвращаем timeout
                return 999.0, 999.0, 999.0
                
            else:
                # На Unix системах
                cmd = ["ping", "-c", str(count), "-W", "1", host]
                output = subprocess.check_output(cmd, universal_newlines=True)
                times = re.findall(r"time=(\d+.\d+)", output)
                if times:
                    times = [float(t) for t in times]
                    return min(times), sum(times)/len(times), max(times)
                    
        except subprocess.CalledProcessError as e:
            logger.error(f"Error pinging {host}: {str(e)}")
            if hasattr(e, 'output'):
                logger.debug(f"Ping output: {e.output}")
        except Exception as e:
            logger.error(f"Unexpected error while pinging {host}: {str(e)}")
            
        return 999.0, 999.0, 999.0  # Возвращаем высокое значение вместо 0, чтобы показать проблему
    
    def analyze_route(self, host: str) -> List[Dict[str, float]]:
        """
        Анализирует маршрут до хоста используя traceroute/tracert
        Returns: список хопов с их пингами
        """
        hops = []
        try:
            if self.platform == "windows":
                cmd = ["tracert", "-d", host]
                # Используем специальную кодировку для Windows
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=startupinfo,
                    universal_newlines=False
                )
                output, error = process.communicate()
                output = output.decode('cp866')
            else:
                cmd = ["traceroute", "-n", host]
                output = subprocess.check_output(cmd, universal_newlines=True)
            
            logger.debug(f"Traceroute output: {output}")
            
            # Парсим вывод
            lines = output.split("\n")
            for line in lines:
                if re.search(r"\d+\s+\d+\s+мс", line, re.IGNORECASE):
                    ip = re.findall(r"\d+\.\d+\.\d+\.\d+", line)
                    times = re.findall(r"(\d+)\s+мс", line, re.IGNORECASE)
                    if ip and times:
                        hops.append({
                            "ip": ip[0],
                            "ping": float(times[0])
                        })
                        
        except subprocess.CalledProcessError as e:
            logger.error(f"Error tracing route to {host}: {str(e)}")
            if hasattr(e, 'output'):
                logger.debug(f"Traceroute output: {e.output}")
        except Exception as e:
            logger.error(f"Unexpected error while tracing route to {host}: {str(e)}")
            
        return hops
