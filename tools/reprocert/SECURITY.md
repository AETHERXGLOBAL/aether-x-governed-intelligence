# Security Policy

## Supported version

ReproCert is currently public alpha software. Only the latest commit on the supported branch is actively maintained during incubation.

## Core security boundary

A ReproCert claim contains a command to execute. Treat a claim-file change as code execution capability.

- Do not run claims from untrusted pull requests with secrets available.
- Use least-privilege GitHub Actions permissions.
- Do not use `pull_request_target` to execute untrusted contribution code.
- ReproCert does not capture environment-variable values.
- Commands are executed with `shell=False` and must be expressed as an argument array.
- Evidence and source paths are constrained to the claim working directory.

## Reporting

Do not place credentials, private customer data, or confidential exploit details in public issues. Use the organization's established private security/contact channel for sensitive reports.
