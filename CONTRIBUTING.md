# Contributing to Nexus-Agent

We welcome contributions from developers of all backgrounds!

## How to Contribute

1. **Fork the Repository**: Fork and clone your own copy.
2. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/awesome-new-tool
   ```
3. **Set Up Development Environment**:
   ```bash
   pip install -e ".[dev]"
   ```
4. **Run Tests**:
   Ensure all tests pass before submitting code:
   ```bash
   pytest -v
   ```
5. **Code Style**:
   - Adhere to PEP 8 standards.
   - All tools must use Pydantic models for argument schemas.
   - Keep functions well-typed and documented.

## Submitting Pull Requests
- Provide a clear description of the feature or bugfix.
- Include unit tests verifying your changes in `tests/`.
- Ensure GitHub Actions CI passes on all matrix configurations.
