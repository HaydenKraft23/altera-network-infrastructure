import copy
import ipaddress
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from analyze_telemetry import analyze
from validate_inventory import validate_inventory


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'fixtures/inventory.json').read_text())

    def test_valid(self):
        self.assertEqual(validate_inventory(self.data), 4)

    def test_missing_simulation_marker(self):
        self.data.pop('simulated')
        with self.assertRaises(ValueError):
            validate_inventory(self.data)

    def test_duplicate_address(self):
        self.data['devices'][1]['address'] = self.data['devices'][0]['address']
        with self.assertRaises(ValueError):
            validate_inventory(self.data)

    def test_private_address_rejected(self):
        self.data['devices'][0]['address'] = str(ipaddress.IPv4Address(167772161))
        with self.assertRaises(ValueError):
            validate_inventory(self.data)

    def test_public_address_rejected(self):
        self.data['devices'][0]['address'] = str(ipaddress.IPv4Address(134744072))
        with self.assertRaises(ValueError):
            validate_inventory(self.data)

    def test_ipv6_rejected(self):
        self.data['devices'][0]['address'] = '::1'
        with self.assertRaises(ValueError):
            validate_inventory(self.data)

    def test_duplicate_name(self):
        self.data['devices'][1]['name'] = self.data['devices'][0]['name']
        with self.assertRaises(ValueError):
            validate_inventory(self.data)

    def test_empty_inventory(self):
        self.data['devices'] = []
        with self.assertRaises(ValueError):
            validate_inventory(self.data)


class TelemetryTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'fixtures/telemetry.json').read_text())

    def test_expected_analysis(self):
        relays = analyze(self.data)['relays']
        self.assertEqual(sum(item['samples'] for item in relays.values()), 192)
        first, second = relays['SOL-RELAY-01'], relays['SOL-RELAY-02']
        self.assertEqual(first['samples'], 96)
        self.assertEqual(first['degraded_samples'], 8)
        self.assertEqual(second['degraded_samples'], 0)
        self.assertEqual(first['mean_rtt_ms'], 38.66)
        self.assertEqual(second['mean_rtt_ms'], 42.49)

    def test_unmarked_data(self):
        self.data['simulated'] = False
        with self.assertRaises(ValueError):
            analyze(self.data)

    def test_bad_numbers(self):
        for field, value in [('rtt_ms', -1), ('rtt_ms', float('nan')),
                             ('rtt_ms', True), ('packet_loss_pct', 101),
                             ('throughput_mbps', float('inf'))]:
            with self.subTest(field=field, value=value):
                data = copy.deepcopy(self.data)
                data['samples'][0][field] = value
                with self.assertRaises(ValueError):
                    analyze(data)

    def test_bad_timestamp(self):
        self.data['samples'][0]['timestamp_utc'] = 'yesterday'
        with self.assertRaises(ValueError):
            analyze(self.data)

    def test_duplicate_sample(self):
        self.data['samples'].append(copy.deepcopy(self.data['samples'][0]))
        with self.assertRaises(ValueError):
            analyze(self.data)

    def test_empty_data(self):
        self.data['samples'] = []
        with self.assertRaises(ValueError):
            analyze(self.data)

    def test_missing_metric(self):
        del self.data['samples'][0]['rtt_ms']
        with self.assertRaises(ValueError):
            analyze(self.data)

    def test_cli_rejects_malformed_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.json'
            path.write_text('{not json', encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/analyze_telemetry.py'), str(path)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn('Analysis failed', result.stderr)


if __name__ == '__main__':
    unittest.main()
