===========================================================
Trame Sandtank
===========================================================

ParFlow sandtank using trame


* Free software: Apache Software License


Development
-----------------------------------------------------------

Create a virtual environment


.. code-block:: console

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -U pip


Build and install ParFlow if not available on your system.
Please look are Linux.readme or MacM1.readme for additional system requiements.

.. code-block:: console

    ./parflow/build-parflow.sh
    ./parflow/build-ecoslim.sh

Build and install the Vue components

.. code-block:: console

    cd vue-components
    npm i
    npm run build
    cd -

Install the application

.. code-block:: console

    pip install -e .


Run the application

.. code-block:: console

    source ./parflow/activate.sh # Only if parflow is not already available
    trame-sandtank --input ./templates/default --output ./data

Usage / testing
-----------------------------------------------------------

You will need to run the following set of command line once

.. code-block:: console

    # get code
    git clone git@github.com:HydroFrame-ML/trame-sandtank.git
    cd trame-sandtank

    # create venv
    python3 -m venv .venv # use 3.9 on Mac M1
    source .venv/bin/activate
    pip install -U pip

    # create a local ParFlow + EcoSLIM
    ./parflow/build-parflow.sh
    ./parflow/build-ecoslim.sh

    # install sandtank
    pip install .


Then once your environment is setup, you can execute the sandtank
application by running the following command lines.

.. code-block:: console

    # Activate venv + parflow
    source .venv/bin/activate
    source ./parflow/activate.sh

    # Run a given template
    trame-sandtank --input ./templates/default --output ./data

To use your own ParFlow + EcoSLIM just set **PARFLOW_DIR** and **ECOSLIM_EXEC** environment variables.

To try within Jupyter once you've installed it by `pip install jupyterlab`

.. code-block:: console

    # Activate venv + parflow
    source .venv/bin/activate
    source ./parflow/activate.sh

    # Run a given template
    jupyter-lab
