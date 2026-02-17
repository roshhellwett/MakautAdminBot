# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in Project Monolith, please report it responsibly:

1. **Do NOT open a public GitHub issue** for security vulnerabilities.
2. Email the maintainer directly at the contact listed on the [Zenith Open Source Projects](https://zenithopensourceprojects.vercel.app/) website.
3. Include a clear description of the vulnerability, steps to reproduce, and potential impact.

### What to Expect
- **Acknowledgment**: Within 48 hours of your report.
- **Resolution**: We aim to patch confirmed vulnerabilities within 7 days.
- **Credit**: Reporters will be credited in the changelog unless they prefer to remain anonymous.

## Security Best Practices

- Never commit `.env` files or API tokens to the repository.
- Always set a strong, random `WEBHOOK_SECRET` in production.
- Keep all dependencies updated to their latest patch versions.
