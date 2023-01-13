# moz-profiler

CLI tool for profiling Mozilla Conduit applications. Currently compatible with: MozPhab.

## Setup

After cloning this repo, execute the following commands:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

To confirm the setup worked, you can run `moz-profiler -h`.

## Usage

To begin using the profiler, navigate to the directory of the application you're profiling.

Currently, it only supports MozPhab, so it should be `review/`. Then execute:

```bash
moz-profiler attach moz-phab
```

This will do a couple of things:

- it should detect your `.bashrc` and add some environment variables
- creates a virtual environment in the directory for its usage
- installs any dependencies in the environment

This updates your `PATH` to include `moz-profiler/bin`, which will intercept any calls made to `moz-phab`,
and forward them to the profiler.

After its attached, it will start storing profiles in `moz-profiler/.profiles`.

`snakeviz` is a dependency, so if you want to inspect any of the profiles, run `snakeviz PROFILE_PATH`.

You can also execute `moz-profiler diff` for a simple comparison between the last two profiles.

When you no longer wish to profile the application, execute `moz-profiler detach moz-phab`.
