# Fiorino.AI

Fiorino.AI is a FastAPI-based server that exposes APIs for AI-related functionalities.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/Fiorino.AI.git
   cd Fiorino.AI
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Update dependencies (optional):
   ```
   pip install --upgrade fastapi uvicorn pydantic pydantic-settings
   pip freeze > requirements.txt
   ```

## Usage

To run the server, use the following command:

```
python run.py
```

The server will start on `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

## Development

To run the server in debug mode, set the `DEBUG` environment variable to `True`:

```
DEBUG=True python run.py
```

## Testing

To run the tests, use the following command:

```
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
