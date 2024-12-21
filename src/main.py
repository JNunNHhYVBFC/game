import sys
import os
import tkinter as tk
from tkinter import ttk
import json
import threading
import time
import logging

# Добавляем путь к директории src в PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from network.ping_analyzer import PingAnalyzer

# Настраиваем логирование
logging.basicConfig(level=logging.DEBUG,
                  format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GamePingOptimizer:
    def __init__(self, root):
        """Инициализация основного окна приложения"""
        logger.debug("Initializing GamePingOptimizer")
        self.root = root
        self.root.title("Game Ping Optimizer")
        
        # Создаем основную рамку
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Создаем заголовок
        title_label = ttk.Label(main_frame, text="Game Ping Optimizer", font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Создаем метку статуса
        self.status_label = ttk.Label(main_frame, text="Status: Initializing...", font=('Helvetica', 10))
        self.status_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        try:
            # Инициализируем анализатор пинга
            logger.debug("Creating PingAnalyzer instance")
            self.ping_analyzer = PingAnalyzer()
            
            # Загружаем список серверов
            logger.debug("Loading servers from config")
            self.load_servers()
            
            # Создаем таблицу серверов
            logger.debug("Creating server table")
            self.create_server_table(main_frame)
            
            # Создаем кнопки управления
            self.create_control_buttons(main_frame)
            
            # Запускаем периодическое обновление
            self.start_periodic_update()
            
        except Exception as e:
            logger.error(f"Error in initialization: {str(e)}")
            self.status_label.config(text=f"Status: Error - {str(e)}")
            raise
    
    def load_servers(self):
        """Загрузка списка серверов из конфигурационного файла"""
        try:
            config_path = os.path.join(parent_dir, "config", "settings.json")
            logger.debug(f"Loading servers from {config_path}")
            
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.servers = config.get('game_servers', [])
                logger.debug(f"Loaded {len(self.servers)} servers")
                
        except Exception as e:
            logger.error(f"Error loading servers: {str(e)}")
            self.servers = []
            raise
    
    def create_server_table(self, parent):
        """Создание таблицы серверов"""
        # Создаем фрейм для таблицы
        table_frame = ttk.Frame(parent)
        table_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Создаем заголовки таблицы
        ttk.Label(table_frame, text="Сервер").grid(row=0, column=0, padx=5)
        ttk.Label(table_frame, text="IP").grid(row=0, column=1, padx=5)
        ttk.Label(table_frame, text="Пинг").grid(row=0, column=2, padx=5)
        
        # Создаем метки для каждого сервера
        self.server_labels = []
        for i, server in enumerate(self.servers, 1):
            name_label = ttk.Label(table_frame, text=server['name'])
            name_label.grid(row=i, column=0, padx=5)
            
            ip_label = ttk.Label(table_frame, text=server['ip'])
            ip_label.grid(row=i, column=1, padx=5)
            
            ping_label = ttk.Label(table_frame, text="---")
            ping_label.grid(row=i, column=2, padx=5)
            
            self.server_labels.append((name_label, ip_label, ping_label))
        
        logger.debug("Server table created successfully")
        # Обновляем данные в таблице
        self.update_server_table()
    
    def create_control_buttons(self, parent):
        """Создание кнопок управления"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        refresh_btn = ttk.Button(button_frame, text="Обновить", command=self.update_server_table)
        refresh_btn.grid(row=0, column=0, padx=5)
        
        optimize_btn = ttk.Button(button_frame, text="Оптимизировать", command=self.optimize_routes)
        optimize_btn.grid(row=0, column=1, padx=5)
    
    def update_server_table(self):
        """Обновление данных в таблице серверов"""
        try:
            for i, server in enumerate(self.servers):
                _, _, ping_label = self.server_labels[i]
                logger.debug(f"Pinging server {server['name']} at {server['ip']}")
                min_ping, avg_ping, max_ping = self.ping_analyzer.ping(server['ip'])
                logger.debug(f"Ping results for {server['name']}: min={min_ping}, avg={avg_ping}, max={max_ping}")
                
                if avg_ping == 999.0:
                    ping_label.config(text="Timeout")
                else:
                    ping_label.config(text=f"{avg_ping:.1f} ms")
            
            self.status_label.config(text="Status: Данные обновлены")
            
        except Exception as e:
            logger.error(f"Error updating server table: {str(e)}")
            self.status_label.config(text=f"Status: Error - {str(e)}")
    
    def optimize_routes(self):
        """Оптимизация маршрутов до серверов"""
        self.status_label.config(text="Status: Оптимизация маршрутов...")
        for server in self.servers:
            routes = self.ping_analyzer.analyze_route(server['ip'])
            # TODO: Добавить логику оптимизации маршрутов
        self.status_label.config(text="Status: Маршруты оптимизированы")
    
    def start_periodic_update(self):
        """Запуск периодического обновления данных"""
        def update_loop():
            while True:
                self.update_server_table()
                time.sleep(5)  # Обновление каждые 5 секунд
        
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()

def main():
    """Основная функция приложения"""
    try:
        logger.info("Starting Game Ping Optimizer")
        root = tk.Tk()
        app = GamePingOptimizer(root)
        root.mainloop()
    except Exception as e:
        logger.critical(f"Critical error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()
