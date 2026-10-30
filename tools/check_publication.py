"""Guard against common publication mistakes; not a full secret scanner."""

import ipaddress
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_SUFFIXES = {'.md', '.py', '.ps1', '.json', '.svg', '.yml', '.yaml', '.example'}
ALLOWED_NAMES = {'.gitignore', '.gitattributes'}
DOCUMENTATION = tuple(ipaddress.ip_network(net) for net in
                      ('192.0.2.0/24', '198.51.100.0/24', '203.0.113.0/24'))
PATTERNS = {
    'private key': r'-----BEGIN (?:RSA |EC |OPENSSH |ENCRYPTED )?PRIVATE KEY-----',
    'GitHub token': r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,})\b',
    'embedded credential URL': r'https?://[^\s/:]+:[^\s/@]+@',
    'original lab hostname': r'\bad\.altera\.test\b',
    'local user path': r'(?i)C:[/\\]Users[/\\]',
    'secret assignment': r'''(?im)^\s*(?:password|shared_secret|api_token|secret_key)\s*[:=]\s*["']?[^\s#"']+''',
}


def scan(root=ROOT):
    findings, count = [], 0
    for path in sorted(root.rglob('*')):
        if not path.is_file() or any(part in {'.git', '__pycache__'} for part in path.relative_to(root).parts):
            continue
        relative = path.relative_to(root).as_posix()
        count += 1
        if path.suffix not in ALLOWED_SUFFIXES and path.name not in ALLOWED_NAMES:
            findings.append(f'{relative}: unapproved file type')
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (UnicodeError, OSError):
            findings.append(f'{relative}: not readable UTF-8 text')
            continue
        for label, pattern in PATTERNS.items():
            if re.search(pattern, text):
                findings.append(f'{relative}: {label}')
        for match in re.finditer(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])', text):
            try:
                address = ipaddress.ip_address(match.group())
            except ValueError:
                continue
            if address.is_loopback or any(address in net for net in DOCUMENTATION):
                continue
            findings.append(f'{relative}: non-documentation IPv4 address')
    return count, findings


def main():
    count, findings = scan()
    if findings:
        print('\n'.join(findings), file=sys.stderr)
        return 1
    print(f'Publication guardrail passed for {count} files. Manual review still required.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
