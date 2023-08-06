# StupidBC

StupidBC is a simple Python implementation of a blockchain.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install StupidBC.

```bash
pip install StupidBC
```

## Usage

```python
from blockchain import BlockChain

bc = BlockChain()

for i in range(10):
    new_block = blockchain.create_block(f"Lucas é um gostoso!")
    bc.mine(new_block)
    bc.add_block(new_block)

print(blockchain._chain)
```

## Running Tests

In the terminal, run the following command

```bash
pytest
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgments

- **Lucas Santos** - _Implemented a blockchain in typescript_ - [khaosdoctor](https://github.com/khaosdoctor)
