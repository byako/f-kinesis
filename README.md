# About

A library which takes in an array of records of variable size and splits the input to batches of records (array of arrays) suitably sized for delivery to a system which has following limits:

* maximum size of output record is 1 MB, larger records should be discarded
* maximum size of output batch is 5 MB
* maximum number of records in an output batch is 500

Input for the library is: `[, , , ... , ]`.

Output is: `[, , ..., ]`, where each batch is an array of records just like in the input.

The are assumed to be strings of variable length and they have to pass intact through the system and records should stay in the order that they arrive.

The library can be used in an application which continuously reads large numbers of records from a data source and writes them to an AWS Kinesis Data stream. The library could be used to create optimum batches for sending data to the Kinesis stream.

# Disclaimer

Size limits are assumed to only relate to strings length, not including JSON sctructure overhead for stringified payload delivery, which inevitably is bigger. 


# Example usage

## Install f_kinesis

### From pypi

```
python3 -m pip install --index-url https://test.pypi.org/simple/ f_kinesis
```

### From sources

```
python3 -m pip install ./
```

## Use f_kinesis

### Command line
```
python3
>>> import f_kinesis
>>> result = f_kinesis.optimum(["a", "b", "cc", "ddd", "eeeee", "ffffffff", "ggggggggggggg"], 13, 64)
>>> result
[['a', 'b', 'cc', 'ddd', 'eeeee'], ['ffffffff'], ['ggggggggggggg']]

```

### Full example

See [example](example/)

# About sources

Tox is used for automation of virtual-environments.

## Install tox

```
# python3 -m pip install tox tox-venv
```

# Supported tasks:

- test: run tests in venv
- lint: run linters in venv to do static code analysis
- format: run formatter in venv to autoformat the code
- example: run [example](example/) application that makes use of this module
- example-real: run same example but install latest f_kinesis release from test.pipy.org

## Example task run:

```
tox -e lint
tox -e example
```
