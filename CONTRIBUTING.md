# Contributing to Fiorino.AI

First off, thank you for considering contributing to Fiorino.AI! It's people like you that make Fiorino.AI such a great tool.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct (be respectful, constructive, and collaborative).

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps which reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed after following the steps
- Explain which behavior you expected to see instead and why
- Include any error messages

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- A clear and descriptive title
- A detailed description of the proposed functionality
- Explain why this enhancement would be useful
- List any potential drawbacks
- If possible, outline the implementation approach

### Pull Requests

1. Fork the repo and create your branch from `main`
2. Branch naming convention:

   - `feature/` prefix for new features
   - `fix/` prefix for bug fixes
   - Example: `feature/add-stripe-integration` or `fix/database-connection`

3. If you've added code that should be tested, add tests
4. Ensure the test suite passes (`pytest`)
5. Make sure your code follows the existing code style
6. Write clear, descriptive commit messages. We recommend using [@fede91/aicommit](https://github.com/Fede91/aicommit) for generating commit messages

## Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/fiorino-ai/fiorino-ai.git
   cd Fiorino.AI
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL:

   - Install PostgreSQL if you haven't already
   - Create a new database for Fiorino.AI
   - Update the `DATABASE_URL` in `.env`

5. Run migrations:
   ```bash
   python run.py
   ```

## Testing

We use pytest for our test suite. To run tests:

```bash
pytest
```

For coverage report:

```bash
pytest --cov=app
```

## Database Migrations

When making changes to the database schema:

1. Create a new migration file in the `migrations` directory
2. Follow the existing migration file naming convention
3. Use yoyo-migrations syntax
4. Test the migration both forward and backward

## Documentation

- All documentation and comments should be in English
- Document new code using docstrings
- Update the README.md if needed
- Add comments for complex logic

## Areas for Contribution

Contributions are welcome everywhere in the codebase, including but not limited to:

- New features
- Bug fixes
- Documentation improvements
- Test coverage
- Performance optimizations
- UI/UX improvements
- Database optimizations
- API enhancements

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
