Tutorials
#########


Quickstart Tutorial 1
=====================

We strongly advise to start with `Quickstart Tutorial
<https://mlgenetics.gitlab.io/dnadna/introduction.html#quickstart-tutorial>`_
that guides you through the whole pipeline, from the beginining (simulations) to
the end (predictions).


Quickstart Tutorial 2: Train SPIDNA on an existing dataset
==========================================================

Description of the existing dataset
----------------------------------


Now that you are familiar with the basic usage of dnadna (Quickstart Tutorial),
we will give a slightly more complex example starting from an already simulated
dataset without using the ``one_event`` pre-filled template.

First download and decompress a small dataset available from our `datasets' repo
<https://gitlab.inria.fr/ml_genetics/public/datasets/>`_. You can do it from
your web browser and decompress the file from your file system with your
favorite tool; or you can run the following commands in your terminal:

.. code-block:: bash

	$ wget https://gitlab.inria.fr/ml_genetics/public/datasets/-/raw/main/toy_data.tar.gz
	$ tar -xzf toy_data.tar.gz

You can list the directory:

.. code-block:: bash

	$ ls -l toy_data
	scen_00
	scen_01
	...
	scen_19
	toy_data_params.csv

And subdirectories:

.. code-block:: bash

	$ ls -l toy_data/scen_00/
	00_0.npz
	00_1.npz
	00_2.npz

And check the parameters of your simulations:

.. code-block:: bash

	$ less toy_data/toy_data_params.csv
	scenario_idx,mutation_rate,recombination_rate,event_time,recent_size,event_size,n_replicates,n_samples,segment_length
	0,1e-08,1e-08,1789,16003,16003,3,50,2000000
	1,1e-08,1e-08,181,5811,34937,3,50,2000000
	...
	19,1e-08,1e-08,392,25102,14392,3,50,2000000


From this it seems that you have 20 scenarios (0 to 19) each with 3 replicates
(independent genomic regions). The mutation and recombination rates, number of
replicates and samples, and region length have fixed values, while
``event_time``, ``recent_size`` and ``event_size`` are varying and describing
the demographic model.

With this information you can create your dataset config file. Let's call it
``toy_data_dataset_config.yml`` and simply write the following information in it:


.. code-block:: YAML

	# toy_data/toy_data_dataset_config.yml
	# ...
	data_root: ./toy_data
	dataset_name: toy_data_QS2
	scenario_params_path: toy_data/toy_data_params.csv

	data_source:
	    format: dnadna
	    filename_format: "scen_{scenario}/{scenario}_{replicate}.npz"


You can see that ``filename_format:
"scen_{scenario}/{scenario}_{replicate}.npz"`` is used to match the name
formatting of the toy dataset, e.g. ``scen_00/00_0.npz``, which differs from
dnadna's default naming scheme:
``scenario_{scenario}/{dataset_name}_{scenario}_{replicate}.npz``

Second, ``data_root`` needs the path to the data, which is ``./toy_data`` (or
any other path to where it was downloaded earlier). The ``dataset_name``
parameter describes the dataset we are using. It won't be used afterwards. It is
only important if you use the default filename format (which contains
``{dataset_name}`` as a variable).


.. code-block:: bash

	$ ls -l
	toy_data
	toy_data_dataset_config.yml
	toy_data.tar.gz


You can now initialize a new set of experiments; advisably it will gather all
networks based on the same preprocessing of the data (filtering done once) and
solving the same task.

.. code-block:: bash

	$ dnadna init --dataset-config toy_data_dataset_config.yml toy_task1


This initializes your experiment named ``toy_task1`` in a folder with the same
name. It is the *model_name* that will be used for naming all the logs,
config files and trained networks. You can specify where to create
this folder by adding another parameter after it, the default is the current
directory ``.``.

Task definition and preprocessing
---------------------------------


The previous command created the file
``toy_task1/toy_task1_preprocessing_config.yml`` in which you will specify the
task to be solved. For example, to train regression models predicting the three
demographic parameters, replace:


.. code-block:: YAML

	# toy_task1/toy_task1_preprocessing_config.yml
	# ...
	# description of the parameters the network will be trained on
	learned_params:
	    param1:
	        type: regression
	        loss_func: MSE
	        loss_weight: 1
	        log_transform: false
	        tied_to_position: false
	    param2:
	        type: classification
	        classes: 2
	        loss_func: Cross Entropy
	        loss_weight: 1

with:


.. code-block:: YAML


	# toy_task1/toy_task1_preprocessing_config.yml
	# ...
	# description of the parameters the network will be trained on
	learned_params:
	-   event_time:
	        type: regression
	        log_transform: false
	        loss_func: MSE
	        loss_weight: 1
	        tied_to_position: false
	-   recent_size:
	        type: regression
	        log_transform: true
	        loss_func: MSE
	        loss_weight: 1
	        tied_to_position: false
	-   event_size:
	        type: regression
	        log_transform: true
	        loss_func: MSE
	        loss_weight: 1
	        tied_to_position: false


Note that here we asked for the population sizes to be log-transformed. The
targeted parameters will be standardized during preprocessing.

In the same config file you can detail filtering steps and
training/validation/test splits, see `Data preprocessing
documentation <https://mlgenetics.gitlab.io/dnadna/data_preprocessing.html>`_ for
more details.

Now run:

.. code-block:: bash

	$ dnadna preprocess toy_task1/toy_task1_preprocessing_config.yml

Network definition and training
-------------------------------


The previous command line outputted ``toy_task1/toy_task1_training_config.yml``
that you can edit to specify anything related to training (network, optimizer,
...). To train a SPIDNA model, replace the network currently in the config file
with:

.. code-block:: YAML

	# toy_task1/toy_task1_training_config.yml
	# ...
	network:
	    name: SPIDNA
	    # net parameters
	    params:
	      n_blocks: 7
	      n_features: 50

SPIDNA can handle batches of varying size. For this demo however, we will
enforce cropping to the 400 first SNPs only; add or update the ``max_snp``
parameter of the ``crop`` function in
``toy_task1/toy_task1_training_config.yml`` as follows:

.. code-block:: YAML

	# toy_task1/toy_task1_training_config.yml
	# ...
	dataset_transforms:
	-   crop:
	        max_snp: 400
	        max_indiv: null
	        keep_polymorphic_only: true
	-   snp_format: concat
	-   validate_snp:
	        uniform_shape: false

Since we had not enforced ``min_snp`` to ``400`` in the preprocessing config
file, some replicates might have less than 400 SNPs. Those are currently padded
to reach 400 when creating batches. To avoid this behavior you can set the
``batch_size`` to ``1`` (although this will substantially slow done training).
In the latter case, since ``min_snp`` was not set, each of this bacth of size 1
might have a different input size; which SPIDNA can handle, contrary to some
neural networks (such as a completely fully connected one).

Finally, you can increase the number of epochs (``n_epochs``) and the number of
batches processed between each validation step (``evaluation_interval``).


See `Model training
documentation <https://mlgenetics.gitlab.io/dnadna/training.html>`_ for
more details on available training options (number of epochs, evaluation interval, ...).

To train this first model, run:


.. code-block:: bash

	$ dnadna train toy_task1/toy_task1_training_config.yml


Repeat as many training runs as desired after changing the parameters described
in ``toy_task1_training_config.yml`` (the full config file is saved within each
run directory for reproducibility).

At any step, visualize the training and validation losses with:

.. code-block:: bash

	$ tensorboard --logdir toy_task1/


For using the trained network on specific datasets, see `Prediction
documentation <https://mlgenetics.gitlab.io/dnadna/prediction.html>`_


Predicting size fluctuations with a pre-trained network (Sanchez et al. 2020)
=============================================================================


We provide `a notebook
<https://gitlab.com/mlgenetics/dnadna/-/tree/master/examples/example_predict_popsize_with_pretrained_spidna.ipynb>`_
reproducing an example of effective population size history inference performed
by the SPIDNA deep learning method described in the paper "Deep learning for
population size history inference: design, comparison and combination with
approximate Bayesian computation" (Sanchez et al. 2020). You should first
install dnadna package by following the `instructions
<https://mlgenetics.gitlab.io/dnadna/introduction.html#installation>`_.

In this notebook, we will simulate SNP data for six scenarios with population
size history defined by hand (e.g. expansion, decline or bottleneck) and use a
pretrained version of SPIDNA to reconstruct these population size histories.
This architecture has been trained using data generated with **msprime** and the
priors described in Sanchez et al. (2020) methods section. Therefore, using the
same architecture to infer the population size histories from datasets falling
outside of this prior might lead to high prediction errors.
