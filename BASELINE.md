# Fiorino.AI Code Base Line Guide

## Key Components

1. **FastAPI Application**: The main application is defined in `app/main.py`.
2. **Database**: SQLAlchemy is used for ORM, configured in `app/db/database.py`.
3. **Configuration**: Project settings are managed in `app/core/config.py`.
4. **API Routes**: Defined in `app/api/routes.py`.
5. **Models**: SQLAlchemy models are defined in `app/models/`.
6. **Migrations**: Yoyo-migrations is used for database migrations.

## Best Practices

1. **Environment Variables**: Use `app/core/config.py` to manage environment variables.
2. **Database Operations**: Always use the `get_db` dependency for database sessions.
3. **API Versioning**: Prefix all routes with `/api` for future versioning.
4. **Model Definition**: Keep SQLAlchemy models in separate files under `app/models/`.
5. **Migrations**: Create a new migration file for each database schema change.
6. **Type Hinting**: Use type hints in function definitions for better code readability.
7. **Error Handling**: Implement proper error handling and return appropriate HTTP status codes.

## Development Workflow

1. Activate the virtual environment:

   ```
   source venv/bin/activate
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run migrations:

   ```
   python run.py
   ```

4. Start the development server:

   ```
   python run.py
   ```

5. For new features:

   - Create a new branch
   - Implement the feature
   - Write tests
   - Create a pull request

6. Before committing:
   - Run tests
   - Check code formatting (consider using `black` or `flake8`)

## Deployment

- The application is designed to be deployed on any platform that supports Python and PostgreSQL.
- Ensure all environment variables are properly set in the production environment.
- Use a production-grade ASGI server like Gunicorn with Uvicorn workers.

## Future Considerations

- Implement authentication and authorization
- Set up CI/CD pipelines
- Integrate with monitoring and logging services
- Implement rate limiting for API endpoints
- Consider caching strategies for frequently accessed data

Remember to keep this guide updated as the project evolves.
