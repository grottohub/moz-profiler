# moz-profiler
simple script for profiling moz tools

currently set up to run a cProfile on moz-phab, but planning on making it more dynamic, user friendly, and powerful

## Setup

I recommend [snakeviz](https://jiffyclub.github.io/snakeviz/) for inspecting profiles, other than that there are no other requirements.

## Usage

Currently it only supports the `moz-phab patch` command, I plan on extending this as well.

```bash
python main.py D1234
```