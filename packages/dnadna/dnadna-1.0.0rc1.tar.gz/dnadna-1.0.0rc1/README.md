# DNADNA

 [![documentation](https://img.shields.io/badge/documentation-latest-success)](https://mlgenetics.gitlab.io/dnadna/) [![pipeline status](https://gitlab.com/mlgenetics/dnadna/badges/master/pipeline.svg)](https://gitlab.com/mlgenetics/dnadna/pipelines/master/latest) [![coverage report](https://gitlab.com/mlgenetics/dnadna/badges/master/coverage.svg?job=test:cuda)](https://mlgenetics.gitlab.io/dnadna/coverage/cuda/)

Deep Neural Architecture for DNA.

The goal of this package is to provide utility functions to improve
development of neural networks for population genetics.

`dnadna` should allow researchers to focus on their research project, be it the
analysis of population genetic data or building new methods, without the need to
focus on proper development methodology (unit test, continuous integration,
documentation, etc.). Results will thus be more easily reproduced and shared.
Having a common interface will also decrease the risk of bugs.


# Installation

## Using conda/mamba

Because DNADNA has some non-trivial dependencies (most notably
[PyTorch](https://pytorch.org/)) the easiest way to install it is in a conda
environment.
We will show how to install it with `mamba` (which is a faster
implementation of `conda`). **Note that all following commands will work with**
`conda` **instead of** `mamba`**, unless otherwise specified.**

If you don't have `conda` yet, follow the [official
instructions](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
to install either the full
[Anaconda](https://docs.conda.io/projects/conda/en/latest/glossary.html#anaconda-glossary)
distribution or, advisably, the smaller
[Miniconda](https://docs.conda.io/projects/conda/en/latest/glossary.html#miniconda-glossary)
distribution.
Once you've installed `conda`, you can follow the
[Mamba](https://github.com/mamba-org/mamba#installation) installation.

You can install DNADNA in an existing conda environment, but the easiest way
is to install it with `mamba` in a new environment.  Start by creating a new
environment:

```console
$ mamba create -n dnadna
```

where the name of the environment (`-n`) is `dnadna` (it won't install
DNADNA yet).

Activate the environment with `mamba activate dnadna`.

Then DNADNA can be installed and updated by running:

```console
$ mamba install -c mlgenetics -c pytorch -c bioconda -c conda-forge dnadna
```

Each `-c` flag specifies a conda "channel" that needs to be searched for
some of the dependencies.  If you want to add the "mlgenetics" channel and
those of its dependencies to your list of default conda channels, you can
run:

```console
$ conda config --add channels mlgenetics \
               --add channels pytorch \
               --add channels conda-forge \
               --add channels bioconda
```

Note: The previous command works only with `conda`, not with `mamba` (yet)


One can make sure `dnadna` is properly installed by running `dnadna -h`.

### Optional dependencies

DNADNA supports logging losses (and eventually other statistics) during
training in the [TensorBoard](https://www.tensorflow.org/tensorboard) format
for better [loss
visualization](https://mlgenetics.gitlab.io/dnadna/training.html#visualize-losses).

To ensure TensorBoard support is enabled, you can install it in your active
conda environment with:

```console
$ mamba install -c conda-forge tensorboard
```

DNADNA can be used inside Jupyter notebooks. If you are using conda/mamba environments, you need to install jupyterlab in the same environement as DNADNA:

```console
$ mamba activate dnadna
$ mamba install -c conda-forge jupyterlab
```


## Using PyPI

If you prefer not to use conda, and to get DNADNA and its dependencies
directly using PyPI+pip you can run:

```console
$ pip install dnadna
```

Note: We still advise to install it within a conda environment.

## Development

Alternatively, you may *clone* the DNADNA git repository and install from
there:

```console
$ git clone https://gitlab.com/mlgenetics/dnadna.git
$ cd dnadna
$ mamba env create
$ mamba activate dnadna
$ pip install .
```

Or using the lighter CPU-only environment:

```console
$ git clone https://gitlab.com/mlgenetics/dnadna.git
$ cd dnadna
$ mamba env create --file environment-cpu.yml
$ mamba activate dnadna-cpu
$ pip install .
```

If you plan to do **development** on the package, it is advisable to choose
the `git clone` solution and install in "editable" mode by running instead:
```console
$ pip install -e .
```

## Updating

If installed with conda/mamba, DNADNA can be updated by running:

```console
$ mamba update -c mlgenetics -c pytorch -c conda-forge dnadna
```

Or, if you already added the release channels to your default channels,
with simply:

```console
$ mamba update dnadna
```

## Note for internal users/developers

Users of the private repository on https://gitlab.inria.fr should see
[the development
documentation](https://mlgenetics.gitlab.io/dnadna/development.html) for
notes on how to access the private repository.


## Docker

A
[Dockerfile](https://gitlab.com/mlgenetics/dnadna/-/blob/master/Dockerfile)
is also included for building a Docker image containing DNADNA (it is based
on conda, so it essentially recreates the installation environment explained
above, including GPU support.  To build the image run:

```console
$ docker build --tag dnadna .
```

Make sure to run this from the root of the repository, as the entire
repository needs to be passed to the Docker build context.

If run without specifying any further commands, it will open a shell with
the `dnadna` conda environment enabled:

```console
$ docker run -ti dnadna
```

However, you can also run it non-interactively, e.g. by specifying the
`dnadna` command.  Here it is also likely a good idea to mount the data
directory for your simulation/training files.  For example:

```console
$ docker run -t -v /path/to/my/data:/data --workdir /data dnadna dnadna init
```

Additional notes on the Docker image:

* By default it logs in as a non-root user named "dnadna" with UID 1001
  and GID also of 1001.  If you start the container with the `--user` flag
  and your own UID it will change the UID and GID of the "dnadna" user.
  Make sure to specify both a UID and a GID, otherwise the group of all
  files owned by "dnadna" will be changed to "root".  E.g., run:
  `docker run -u $(id -u):$(id -g)`.

* The default workdir is `/home/dnadna/dnadna` which contains the `dnadna`
  package source code.

* If you want to install your own conda packages (e.g. to use this container
  for development), after starting the container it is best to create a new
  conda environment cloned from the base environment, then re-install
  dnadna:

  ```console
  $ conda create -n dnadna --clone base
  $ conda activate dnadna
  $ pip install -e .
  ```

  This is not done by default by the image because it would require
  additional start-up time in the non-development case.  However, as
  a short-cut for the above steps you can run the container with
  `docker run -e DEV=1`.

  Afterwards, you can create a snapshot of this container in another
  terminal, e.g. by running `docker commit <my-container> dnadna-dev`.


# Dependencies

- python >= 3.6
- pytorch
- pandas
- numpy
- matplotlib
- msprime
- jsonschema
- pyyaml
- tqdm

(For a complete list, see `setup.cfg`, or `requirements.txt`.)


# Quickstart Tutorial

After successful installation you should have a command-line utility called
`dnadna` installed:

```console
$ dnadna --help
usage: dnadna [-h] [COMMAND]

dnadna version ... top-level command.

See dnadna <sub-command> --help for help on individual sub-commands.

optional arguments:
  -h, --help       show this help message and exit
  --plugin PLUGIN  load a plugin module; the plugin may be specified either as the file path to a Python module, or the name of a module importable on the current Python module path (i.e. sys.path); plugins are just Python modules which may load arbitrary code (new simulators, loss functions, etc.) during DNADNA startup); --plugin may be passed multiple times to load multiple plugins
  --trace-plugins  enable tracing of plugin loading; for most commands this is enabled by default, but for other commands is disabled to reduce noise; this forces it to be enabled
  -V, --version    show the dnadna version and exit

sub-commands:
  init          Initialize a new model training configuration and directory
                structure.
  preprocess    Prepare a training run from an existing model training
                configuration.
  train         Train a model on a simulation using a specified pre-processed
                training config.
  predict       Make parameter predictions on existing SNP data using an already
                trained model.
  simulation    Run a registered simulation.
```

This implements a number of different sub-commands for different training
and simulation steps.  The `dnadna` command can be used either starting with
an existing simulation dataset (which may need to be first be converted to
the [DNADNA Dataset
Format](https://mlgenetics.gitlab.io/dnadna/datasets.html#the-dnadna-dataset-format),
or you may use `dnadna`'s simulator interface to create a new simulation
dataset.

Here we step through the complete process from configuring and generating a
simulation, to running data pre-processing on the simulation, and training a
network based off that simulation.

If you already have simulation data in the [DNADNA Data
Format](#data-format) you can skip straight to the
[initialization](#model-initialization) step.


## Simulation initialization and configuration

To initialize a simulation, we must first generate a config file and output
folder for it, using the `dnadna simulation init` command:

```console
$ dnadna simulation init my_dataset one_event
Writing sample simulation config to my_dataset/my_dataset_simulation_config.yml ...
Edit the config file as needed, then run this simulation with the command:

    dnadna simulation run my_dataset/my_dataset_simulation_config.yml
```

This will create a directory in the current directory, named `my_dataset/`,
and initialize it with a config file pre-populated with sample parameters
for the built-in [one_event example
simulator](https://mlgenetics.gitlab.io/dnadna/_autosummary/_autosummary/dnadna.examples.one_event.html).

Before running the simulation we may want to adjust some of the parameters.
Open `my_dataset/my_dataset_simulation_config.yml` in your favorite text
editor.  By default we see that `n_scenarios` is `100` with `n_replicates`
of 3 per scenario (in the one_event example `n_replicates` is the number of independently simulated genomic regions). You can change it to `20` scenarios with `2` replicates, i.e. 100 simulations total, which is good for this quick demo but too low for training a real model. For a real training with enough computing resources, we would recommend changing these numbers to higher values such as `20000` and `100` (2 million simulations which take a very long time). You may
also set the `seed` option to seed the random number generator for
reproducible results.  The resulting file (with none of the other settings
changed) should look like:

```yaml
# my_dataset/my_dataset_simulation_config.yml
data_root: .
n_scenarios: 20
n_replicates: 2
seed: 2
...
```

## Running the simulation

Now to run the simulation we configured, we run `dnadna simulation run`,
passing it the path to the config file we just edited.  If you run this in a
terminal it will also display a progress bar:

```console
$ dnadna simulation run my_dataset/my_dataset_simulation_config.yml
... INFO;  Running one_event simulator with n_scenarios=20 and n_replicates=2
... INFO;  Simulation complete!
... INFO;  Initialize model training with the command:
... INFO;
... INFO;      dnadna init --simulation-config=my_dataset/my_dataset_simulation_config.yml <model-name>
```

## Model initialization

The main command for initialize DNADNA is `dnadna init`, which assumes we
already have a simulation (such as the one we just generated) in the
standard [DNADNA Data Format](#data-format).  Although this command can be
run without any arguments (producing a default config file), if we pass it
the path to our simulation config file it will output a config file
appropriate for use with that simulation:

```console
$ dnadna init --simulation-config=my_dataset/my_dataset_simulation_config.yml my_model
Writing sample preprocessing config to my_model/my_model_preprocessing_config.yml ...
Edit the dataset and/or preprocessing config files as needed, then run preprocessing with the command:

    dnadna preprocess my_model/my_model_preprocessing_config.yml
```

After running `dnadna init`, it is expected that the user will manually edit
the sample config file that it outputs, in order to exactly specify how they
want to train their model, and on which parameters.  In fact, the default
template is going to be good enough for our demo simulation, except for one
bit that will give us trouble.

The option `dataset_splits:` has a default value meaning 70% of our
scenarios will be used for training, and only 30% for validation.  Since,
for this quick demo, we only have 20 scenarios, the validation set will be
too small.  Open the file `my_model/my_model_preprocessing_config.yml` in your
editor and change this so that our dataset is split 50/50 between training
and validation:

```yaml
# my_model/my_model_preprocessing_config.yml
# ...
dataset_splits:
    training: 0.5
    validation: 0.5
```

Under normal use you would set these ratios however you prefer.  You can
also include a `test` set of scenarios to be set aside for testing your
model.


## Pre-processing

Before training a model, some data pre-processing must be performed on the
data set; the output of this pre-processing can depend on the settings in
the preprocessing config file that was output by `dnadna init`.  To do this,
simply run:

```console
$ dnadna preprocess my_model/my_model_preprocessing_config.yml
... INFO;  Removing scenarios with:
... INFO;   - Missing replicates
... INFO;   - Fewer than 500 SNPs
... INFO;  ...
... INFO;  Using ... CPU for checking scenarios
... INFO;  20 scenarios out of 20 have been kept, representing 40 simulations
... INFO;  Splitting scenarios between training and validation set
... INFO;  Standardizing continuous parameters
... INFO;  Writing preprocessed scenario parameters to: .../my_model/my_model_preprocessed_params.csv
... INFO;  Writing sample training config to: .../my_model/my_model_training_config.yml
... INFO;  Edit the training config file as needed, then start the training run with the command:
... INFO;
... INFO;      dnadna train .../my_model/my_model_training_config.yml
```

This will produce a `<model_name>_training_config.yml` file containing the
config file prepared for training your model.


## Training

To run a model training, after pre-processing use `dnadna train`, giving it
the path to the pre-processed training config file as output by the last
step.

In order to make the training run a little faster (just for this example)
let's also edit the training config file to limit it to one epoch:

```yaml
# my_model/my_model_training_config.yml
# ...
# name and parameters of the neural net model to train
network:
    name: CustomCNN

# number of epochs over which to repeat the training process
n_epochs: 1
...
```

Then run `dnadna train` on the training config file:

```console
$ dnadna train my_model/my_model_training_config.yml
... INFO;  Preparing training run
... INFO;  20 samples in the validation set and 20 in the training set
... INFO;  Start training
... INFO;  Networks states are saved after each validation step
... INFO;  Starting Epoch #1
... INFO;  Validation at epoch: 1 and batch: 1
... INFO;  Compute all outputs for validation dataset...
... INFO;  Done
... INFO;  training loss = 1.0222865343093872 // validation loss = 1.2975229024887085
... INFO;  Better loss found on validation set: None --> 1.2975229024887085
... INFO;  Saving model to ".../my_model/run_000/my_model_run_000_best_net.pth" ...
... INFO;  Compute all outputs for validation dataset...
... INFO;  Done
... INFO;  --- 3.185938596725464 seconds ---
... INFO;  --- Best loss: 3.892427444458008
... INFO;  Saving model to ".../my_model/run_000/my_model_run_000_last_epoch_net.pth" ...
... INFO;  You can test the model's predictions on a test dataset by running the command:
... INFO;
... INFO;      dnadna predict .../my_model/run_000/my_model_run_000_last_epoch_net.pth <dataset config file or paths to .npz files>
```

By default this will output a directory for your training run under
`model_name/run_NNN` where `NNN` is an integer run ID.  The run ID starts at
0, and by default the next unused run ID is used.  However, you may also
pass the `--run-id` argument to give a custom run ID, which may be either an
integer, or an arbitrary string.

Following a successful training run will output a
`<model_name>_run_<run_id>_last_epoch_net.pth` file in the run directory,
containing the final trained model in a pickled format, which can be loaded
by the
[torch.load](https://pytorch.org/docs/stable/torch.html?highlight=torch%20load#torch.load)
function.

Under the run directory this will also produce a
`<model_name>_<run_id>_training_config.yml` file containing the final config
file prepared for this training run.  This contains a complete copy of the
"base" training config use used to run `dnadna train` as well as a
complete copy of the simulation config.  This information is copied in full
for the purpose of provenance and reproducibility of a training run.

The expectation is that between multiple training runs, you may modify
the "base" config to tune the training, either by modifying the original
config file directly, or by copying it and editing the copy.  In any case,
the final configuration used to perform the training run is saved in the run
directory and should not be modified.

You can keep track of all training and validation losses with TensorBoard


## Prediction

Given the trained network, we can now use it to make (or confirm)
predictions on new datasets.  To demonstrate we'll run the `dnadna predict`
model over part of the existing dataset we just used to train the model,
though in practice it could be run on any data that conforms (e.g. in
dimensions) to the dataset the model was trained on.  The output is a CSV
file containing the parameter predictions for each input:

```console
$ dnadna predict my_model/run_000/my_model_run_000_last_epoch_net.pth \
                 my_dataset/scenario_04/*.npz
path,event_time,recent_size,event_size
.../my_dataset/scenario_04/my_dataset_04_0.npz,-0.06392800807952881,-0.11097482591867447,-0.12720556557178497
.../my_dataset/scenario_04/my_dataset_04_1.npz,-0.06392764300107956,-0.11097370833158493,-0.12720371782779694
```


# Data format

DNADNA has a prescribed filesystem layout and file format for the datasets
its works on.  Some of the details of this layout can be modified in the
configuration files, and in a future version will be further customizable by
plugins.

But the default format assumes that SNP data (SNP matrices and associated
SNP position arrays) are stored in NumPy's
[NPZ](https://numpy.org/devdocs/reference/generated/numpy.savez.html#numpy.savez)
format with one file per SNP.  They are organized on disk by scenario like:

```
\_ my_simulation/
    \_ my_simulation_params.csv  # the scenario parameters table
    |_ my_simulation_dataset_config.yml  # the simulation config file
    |_ scenario_000/
        \_ my_simulation_000_00.npz  # scenario 0 replicate 0
        ...
        |_ my_simulation_000_NN.npz
    |_ scenario_001/
        \_ my_simulation_001_00.npz  # scenario 1 replicate 0
        ...
        |_ my_simulation_001_NN.npz
    ...
    |_ scenario_NNN/
        \_ my_simulation_NNN_00.npz
        ...
        |_ my_simulation_NNN_NN.npz
```

The file `my_simulation_params.csv` contains the known target values for
each parameter of the simulation, on a per-scenario basis.  It is currently
a plain CSV file which must contain at a minimum 3 columns:

* A `scenario_idx` column giving the scenario number.
* An `n_replicates` column which specifies the number of replicates in that
  scenario.
* One or more additional columns containing arbitrary parameter names, and
  their values each scenario in the dataset.

For example:

```csv
scenario_idx,mutation_rate,recombination_rate,event_time,n_replicates
0,1e-08,1e-08,0.3865300203456797,-0.497464473948751,100
1,1e-08,1e-08,0.19344551118300793,0.16419897912977574,100
...
```

An associated config file here named `my_simulation_dataset_config.yml`
provides further details about how to load the dataset to the DNADNA
software.  An example dataset config can be generated by running `dnadna
init`.

See [The DNADNA Dataset
Format](https://mlgenetics.gitlab.io/dnadna/simulation.html#the-dnadna-dataset-format)
for more details.

# Development

See [the development
documentation](https://mlgenetics.gitlab.io/dnadna/development.html)
for full details on how to set up and use a development environment and
contribute to DNADNA.


# Detailed usage

For the full usage manual see the [DNADNA
Documentation](https://mlgenetics.gitlab.io/dnadna/overview.html).
