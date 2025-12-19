# MeshChain Development Guide

This guide provides information for developers working on MeshChain.

## Technology Stack

### Core Languages

**Python 3.11+** (Primary)
- Rapid prototyping and development
- Extensive cryptography libraries (PyNaCl, pycryptodome)
- Easy testing and iteration
- Compatible with Meshtastic Python API
- Suitable for embedded systems

**Rust** (Optional, for performance-critical components)
- Ring signature implementation
- Cryptographic operations
- High-performance consensus
- Can be called from Python via FFI

**Go** (Optional, for network layer)
- Concurrent message handling
- Network protocol implementation
- Meshtastic integration
- Can be called from Python via subprocess

### Key Libraries

**Cryptography:**
- `PyNaCl` (libsodium bindings) - Ed25519 signatures, encryption
- `pycryptodome` - AES, SHA-256, additional crypto primitives
- `cryptography` - X.509 certificates, key derivation

**Networking:**
- `meshtastic` - Official Meshtastic Python API
- `asyncio` - Asynchronous networking
- `protobuf` - Message serialization

**Storage:**
- `sqlite3` - Built-in Python SQLite support
- `sqlalchemy` - ORM for database abstraction (optional)

**Testing:**
- `pytest` - Unit testing framework
- `pytest-asyncio` - Async test support
- `pytest-cov` - Code coverage reporting

**Code Quality:**
- `black` - Automatic code formatting (PEP 8)
- `flake8` - Linting and style checking
- `mypy` - Static type checking
- `isort` - Import sorting

**Documentation:**
- `sphinx` - Documentation generation
- `sphinx-rtd-theme` - ReadTheDocs theme

## Project Structure

```
meshchain/
├── meshchain/                  # Main package
│   ├── __init__.py
│   ├── transaction.py         # Transaction handling
│   ├── block.py               # Block structure
│   ├── blockchain.py          # Blockchain management
│   ├── consensus.py           # DPoP consensus
│   ├── crypto.py              # Cryptographic operations
│   ├── wallet.py              # Wallet management
│   ├── network.py             # Meshtastic integration
│   ├── storage.py             # Database operations
│   └── node.py                # Full node implementation
│
├── tests/                      # Unit tests
│   ├── test_transaction.py
│   ├── test_block.py
│   ├── test_consensus.py
│   ├── test_crypto.py
│   ├── test_wallet.py
│   └── conftest.py            # Pytest configuration
│
├── docs/                       # Documentation
│   ├── ARCHITECTURE.md
│   ├── PROTOCOL.md
│   ├── CONSENSUS.md
│   ├── PRIVACY.md
│   ├── API.md
│   └── DEVELOPMENT.md
│
├── examples/                   # Example code
│   ├── simple_node.py
│   ├── create_wallet.py
│   ├── send_transaction.py
│   └── run_testnet.py
│
├── tools/                      # Utility tools
│   ├── cli.py                 # Command-line interface
│   ├── block_explorer.py      # Block explorer
│   └── testnet.py             # Testnet simulator
│
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── requirements.txt
├── requirements-dev.txt
├── setup.py
└── .github/
    └── workflows/
        └── tests.yml          # CI/CD configuration
```

## Development Workflow

### 1. Setting Up Your Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/meshchain.git
cd meshchain

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks (optional)
pre-commit install
```

### 2. Making Changes

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes
# Edit files, add tests, update documentation

# Format code
black meshchain/ tests/

# Check linting
flake8 meshchain/ tests/

# Run type checking
mypy meshchain/

# Run tests
pytest tests/ -v --cov=meshchain

# Commit changes
git add .
git commit -m "Add your feature description"

# Push to GitHub
git push origin feature/your-feature-name
```

### 3. Creating a Pull Request

1. Go to GitHub and create a pull request
2. Fill in the PR template with:
   - Description of changes
   - Related issues
   - Testing performed
   - Screenshots (if applicable)
3. Wait for code review
4. Address any feedback
5. Merge when approved

## Code Style Guide

### Python Style

We follow PEP 8 with these additions:

**Line Length:** 100 characters (not 79)

**Type Hints:** Use for all functions

```python
def calculate_fee(amount: int, rate: float) -> int:
    """Calculate transaction fee."""
    return int(amount * rate)
```

**Docstrings:** Use Google-style docstrings

```python
def process_transaction(tx: Transaction) -> bool:
    """
    Process a transaction.
    
    Args:
        tx: Transaction to process
    
    Returns:
        True if successful, False otherwise
    
    Raises:
        ValueError: If transaction is invalid
    """
    pass
```

**Imports:** Organize in three groups

```python
# Standard library
import hashlib
import struct
from typing import List

# Third-party
import meshtastic
from nacl import signing

# Local
from meshchain.transaction import Transaction
from meshchain.crypto import verify_signature
```

**Constants:** Use UPPER_CASE

```python
MAX_VALIDATORS = 7
BLOCK_TIME_SECONDS = 5
FINALITY_THRESHOLD = 0.66
```

### Naming Conventions

- Classes: `PascalCase` (e.g., `Transaction`, `BlockValidator`)
- Functions/methods: `snake_case` (e.g., `calculate_fee`, `verify_signature`)
- Constants: `UPPER_CASE` (e.g., `MAX_BLOCK_SIZE`)
- Private methods: `_snake_case` (e.g., `_internal_method`)
- Protected methods: `_snake_case` (e.g., `_protected_method`)

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_transaction.py

# Run specific test
pytest tests/test_transaction.py::TestTransaction::test_transaction_creation

# Run with coverage
pytest --cov=meshchain tests/

# Run with verbose output
pytest -v tests/

# Run with specific markers
pytest -m "not slow" tests/
```

### Writing Tests

```python
import pytest
from meshchain.transaction import Transaction

class TestTransaction:
    """Test cases for Transaction class."""
    
    @pytest.fixture
    def sample_tx(self) -> Transaction:
        """Create a sample transaction."""
        return Transaction(...)
    
    def test_transaction_creation(self, sample_tx: Transaction) -> None:
        """Test creating a transaction."""
        assert sample_tx.version == 1
    
    def test_transaction_invalid_amount(self) -> None:
        """Test that invalid amounts are rejected."""
        with pytest.raises(ValueError):
            Transaction(amount=-100)
```

### Coverage Requirements

- Minimum 80% code coverage
- All public functions must have tests
- Test both success and failure cases
- Use descriptive test names

## Debugging

### Using Print Statements

```python
def process_block(block: Block) -> None:
    """Process a block."""
    print(f"Processing block {block.height}")
    print(f"Block hash: {block.hash().hex()}")
    print(f"Transactions: {len(block.transactions)}")
```

### Using the Debugger

```python
import pdb

def process_block(block: Block) -> None:
    """Process a block."""
    pdb.set_trace()  # Debugger will stop here
    # ... rest of code
```

### Using IPython

```bash
# Install IPython
pip install ipython

# Use in code
from IPython import embed
embed()  # Interactive shell will start here
```

## Documentation

### Writing Documentation

- Use Markdown for documentation
- Include code examples
- Update README.md for major changes
- Update ARCHITECTURE.md for design changes
- Add docstrings to all public functions

### Building Documentation

```bash
# Install Sphinx
pip install sphinx sphinx-rtd-theme

# Build HTML documentation
cd docs
make html

# View documentation
open _build/html/index.html
```

## Performance Optimization

### Profiling

```python
import cProfile
import pstats

# Profile a function
profiler = cProfile.Profile()
profiler.enable()

# ... code to profile ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Benchmarking

```python
import timeit

# Benchmark a function
time = timeit.timeit(
    'my_function()',
    setup='from __main__ import my_function',
    number=1000
)
print(f"Average time: {time / 1000} seconds")
```

## Common Development Tasks

### Adding a New Module

1. Create file in `meshchain/` directory
2. Add docstring and type hints
3. Create corresponding test file in `tests/`
4. Update `__init__.py` to export public functions
5. Add documentation in `docs/`

### Adding a New Test

1. Create test file in `tests/` directory
2. Use `test_` prefix for test functions
3. Use descriptive test names
4. Use fixtures for setup/teardown
5. Run tests to verify

### Adding a New Dependency

1. Add to `requirements.txt` (for production)
2. Add to `requirements-dev.txt` (for development)
3. Update `setup.py` if needed
4. Document in README.md
5. Update CONTRIBUTING.md if needed

## Continuous Integration

We use GitHub Actions for CI/CD. Configuration is in `.github/workflows/tests.yml`.

### CI Pipeline

1. Run tests with pytest
2. Check code coverage (minimum 80%)
3. Run linting with flake8
4. Run type checking with mypy
5. Build documentation

### Local CI Testing

```bash
# Run all CI checks locally
black meshchain/ tests/
flake8 meshchain/ tests/
mypy meshchain/
pytest tests/ --cov=meshchain
```

## Release Process

1. Update version in `__init__.py`
2. Update `CHANGELOG.md`
3. Create git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. GitHub Actions will build and publish release

## Getting Help

- **GitHub Issues:** Report bugs and request features
- **GitHub Discussions:** Ask questions and discuss ideas
- **Meshtastic Forums:** Community discussions
- **Pull Request Reviews:** Get feedback on code

## Additional Resources

- [Python PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [Type Hints Documentation](https://docs.python.org/3/library/typing.html)
- [Meshtastic Documentation](https://meshtastic.org/)
- [Bitcoin Protocol](https://en.bitcoin.it/wiki/Protocol_documentation)
- [Monero Research](https://www.getmonero.org/resources/research-lab/)

## Questions?

Feel free to ask in GitHub Discussions or open an issue!
