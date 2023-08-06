Azure Machine Learning Python SDK v2
==============================================================================

.. contents::
    :depth: 1
    :local:

Overview
------------------------------------------------------------------------------
The azure-ai-ml is a Python SDK package (aka AML SDKv2) for Azure Machine Learning, which allows users to:

- Submit training jobs
- Manage data, models, environments
- Perform managed inferencing (real time and batch)
- Stitch together multiple tasks and production workflows using Azure ML pipelines

Use cases for SDK v2
------------------------------------------------------------------------------
The SDK v2 is useful in the following scenarios:

1. Move from simple to complex concepts incrementally. SDK v2 allows you to:
    - Construct a single command.
    - Add a hyperparameter sweep on top of that command
    - Add the command with various others into a pipeline one after the other.

    This construction is useful, given the iterative nature of machine learning.

2. Reusable components in pipelines

    Azure ML introduces `components <https://docs.microsoft.com/azure/machine-learning/concept-component.md>`_ for managing and reusing common logic across pipelines. This functionality is available only via CLI v2 and SDK v2.

3. Managed inferencing

    Azure ML offers `endpoints <https://docs.microsoft.com/azure/machine-learning/concept-endpoints.md>`_ to streamline model deployments for both real-time and batch inference deployments. This functionality is available only via CLI v2 and SDK v2.




Get started with SDK v2
------------------------------------------------------------------------------
- Read through this `Install and set up SDK (v2) <https://aka.ms/sdk-v2-install>`_
- Read through this `Train models with the Azure ML Python SDK v2 (preview) <https://docs.microsoft.com/azure/machine-learning/how-to-train-sdk>`_
- Read through this `Tutorial: Create production ML pipelines with Python SDK v2 (preview) in a Jupyter notebook <https://docs.microsoft.com/azure/machine-learning/tutorial-pipeline-python-sdk.md>`_

Setup
------------------------------------------------------------------------------
    Install the azure-ai-ml package:

        .. code-block:: bash

            pip install --pre azure-ai-ml


Change Log
----------

Initial prerelease
=========================

- initial prerelease
