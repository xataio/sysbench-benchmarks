# Xata benchmark results

This repo contains scripts, configurations used, and results for the benchmarks runs for this [blog post](https://xata.io/blog/reaction-to-the-planetscale-postgresql-benchmarks).

It is based on the [PlanetScale PostgreSQL benchmarks](https://planetscale.com/blog/benchmarking-postgres).

## TPCC-like benchmark

Based on the instructions [here](https://planetscale.com/benchmarks/instructions/tpcc500g).

With the addition of running `CHECKPOINT;` and `VACUUM;` before the start of the benchmark.

In order to create the conditions as close as possible to the original blog post, we have used a `c6a.xlarge` as a in the `us-east-1` region as a test runner. This was outside of our production account.

## Overall results

Note: we have only run the benchmarks against Xata, the rest of the results are from the PlanetScale blog post.

<img width="2612" height="1680" alt="benchmark-all-tpcc-results" src="https://github.com/user-attachments/assets/f149a69f-066e-414a-8e68-c1a5f1a1b92a" />
