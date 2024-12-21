import unittest
from src.network.ping_analyzer import PingAnalyzer

class TestPingAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = PingAnalyzer()
    
    def test_ping_valid_host(self):
        """Тест пинга до валидного хоста"""
        min_ping, avg_ping, max_ping = self.analyzer.ping("8.8.8.8", count=1)
        self.assertIsInstance(min_ping, float)
        self.assertIsInstance(avg_ping, float)
        self.assertIsInstance(max_ping, float)
        self.assertGreaterEqual(min_ping, 0)
        self.assertLessEqual(max_ping, 999)
    
    def test_ping_invalid_host(self):
        """Тест пинга до невалидного хоста"""
        min_ping, avg_ping, max_ping = self.analyzer.ping("invalid.host", count=1)
        self.assertEqual(min_ping, 999.0)
        self.assertEqual(avg_ping, 999.0)
        self.assertEqual(max_ping, 999.0)
    
    def test_analyze_route(self):
        """Тест анализа маршрута"""
        hops = self.analyzer.analyze_route("8.8.8.8")
        self.assertIsInstance(hops, list)
        if hops:  # если есть хопы
            first_hop = hops[0]
            self.assertIn("ip", first_hop)
            self.assertIn("ping", first_hop)
            self.assertIsInstance(first_hop["ping"], float)

if __name__ == '__main__':
    unittest.main()
