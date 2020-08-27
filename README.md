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


# Running tests

```
tox -e test
```


# Running code analysis

```
tox -e lint
```
