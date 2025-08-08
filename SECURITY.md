# Security Policy

## Supported Versions

We actively support the following versions of Inkwell:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you believe you have found a security vulnerability in Inkwell, please report it to us as described below.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please send an email to: security@punyaksirohi.dev (or create a private security advisory through GitHub)

Please include the following information:
- Description of the vulnerability
- Steps to reproduce or proof-of-concept
- Potential impact
- Suggested fix (if any)

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours.
- **Investigation**: We will investigate and validate the vulnerability within 5 business days.
- **Updates**: We will keep you informed of our progress throughout the process.
- **Resolution**: We will work to resolve confirmed vulnerabilities within 30 days.
- **Disclosure**: Once fixed, we will coordinate with you on responsible disclosure.

### Security Best Practices

When deploying Inkwell in production:

1. **Environment Variables**: Always use environment variables for sensitive configuration
2. **Secret Key**: Generate a strong, unique SECRET_KEY for production
3. **Debug Mode**: Ensure DEBUG=False in production
4. **HTTPS**: Always use HTTPS in production
5. **Database**: Use a proper database (PostgreSQL) instead of SQLite
6. **Dependencies**: Keep all dependencies up to date
7. **Static Files**: Serve static files through a web server (nginx/Apache)
8. **Media Files**: Validate and sanitize user uploads

### Security Headers

Inkwell includes several security headers by default:
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block

For production deployments, consider enabling:
- Strict-Transport-Security (HSTS)
- Content-Security-Policy (CSP)
- Referrer-Policy

## Security Updates

Security updates will be released as patch versions and will be announced through:
- GitHub Releases
- GitHub Security Advisories
- Repository README updates

## Responsible Disclosure

We believe in responsible disclosure and will work with security researchers to:
- Understand and reproduce the issue
- Develop and test a fix
- Release the fix in a timely manner
- Publicly acknowledge the researcher (unless they prefer to remain anonymous)

Thank you for helping to keep Inkwell secure!
