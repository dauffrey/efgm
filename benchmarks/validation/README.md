# Validation Benchmark Partition

Cases in this directory are used for periodic comparison of frozen candidate models/configurations after development work.

They should not be repeatedly inspected to micro-tune candidate parameters. Repeated adaptation to this partition turns it into development data and should trigger creation of a new validation set.

Record every candidate evaluation against this partition in an experiment result.
