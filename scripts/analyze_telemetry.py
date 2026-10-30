"""Summarize explicitly synthetic training telemetry; no network access."""

import argparse
from collections import defaultdict
from datetime import datetime
import json
import math
from pathlib import Path
import statistics


def numeric(value, field, low=0, high=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{field} must be numeric')
    if not math.isfinite(value) or value < low or (high is not None and value > high):
        raise ValueError(f'{field} is outside its valid range')
    return value


def analyze(payload):
    if not isinstance(payload, dict) or payload.get('simulated') is not True:
        raise ValueError('Telemetry must be explicitly marked simulated=true')
    samples = payload.get('samples')
    if not isinstance(samples, list) or not samples:
        raise ValueError('samples must be a nonempty list')
    grouped, seen = defaultdict(list), set()
    for sample in samples:
        if not isinstance(sample, dict) or sample.get('simulated') is not True:
            raise ValueError('Every sample must be explicitly simulated')
        relay = sample.get('relay_id')
        if not isinstance(relay, str) or not relay.strip():
            raise ValueError('relay_id must be a nonempty string')
        timestamp = sample.get('timestamp_utc')
        if not isinstance(timestamp, str) or not timestamp.endswith('Z'):
            raise ValueError('timestamp_utc must be an ISO timestamp ending in Z')
        instant = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        key = (relay, instant)
        if key in seen:
            raise ValueError('Duplicate relay/timestamp sample')
        seen.add(key)
        numeric(sample.get('rtt_ms'), 'rtt_ms')
        numeric(sample.get('throughput_mbps'), 'throughput_mbps')
        numeric(sample.get('packet_loss_pct'), 'packet_loss_pct', high=100)
        if not isinstance(sample.get('state'), str) or not sample['state'].strip():
            raise ValueError('state must be a nonempty string')
        grouped[relay].append(sample)
    return {
        'simulated': True,
        'warning': 'Training fixture only; not real satellite performance or failover evidence.',
        'relays': {
            relay: {
                'samples': len(rows),
                'mean_rtt_ms': round(statistics.mean(row['rtt_ms'] for row in rows), 2),
                'peak_loss_pct': max(row['packet_loss_pct'] for row in rows),
                'degraded_samples': sum(row['state'] != 'nominal' for row in rows),
            }
            for relay, rows in sorted(grouped.items())
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('telemetry', type=Path)
    args = parser.parse_args()
    try:
        result = analyze(json.loads(args.telemetry.read_text(encoding='utf-8')))
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Analysis failed: {exc}\n')
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
