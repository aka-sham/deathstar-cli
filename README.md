# Death Star CLI - R2D2

The Death Star CLI project aka R2D2 is a command-line interface written in Python to communicate with the Death Star Backend aka Millenium Falcon.

This project is part of Giskard technical test.

## Getting started

### Prerequisites
- Python 3.10
- PDM 2.1
- Death Star Backend 1.0.0

You need first to install PDM by following [PDM documentation](https://pdm.fming.dev/latest/#installation).

Then at the root directory type the following command in your terminal:

```bash
pdm install
```

### Usage
The CLI communicates with the Death Star Backend project and you must start it first before using R2D2. You also need to create an *.env* file in the root directory with your Death Star Backend URL:

```bash
BACKEND_URL=http://127.0.0.1:8000
```

Finally run the command by providing the 2 json files as parameters:
```bash
pdm r2d2 config/millennium-falcon.json config/empire.json
```

**Note:** there are 2 examples file in the *config* directory.

## Git branching model and workflow

To work efficiently together with Git, OneFlow has been chosen. See [OneFlow – a Git branching model and workflow](https://www.endoflineblog.com/oneflow-a-git-branching-model-and-workflow).

Because this repository is using 2 branches (develop and main), the chosen workflow is the variation with 2 branches with Option #3 to finish a feature branch.
