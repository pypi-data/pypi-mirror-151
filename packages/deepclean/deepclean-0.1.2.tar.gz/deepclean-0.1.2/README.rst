Deep clean
##########

.. image:: https://git.shore.co.il/nimrod/deepclean/badges/main/pipeline.svg
    :target: https://git.shore.co.il/nimrod/deepclean/-/commits/main
    :alt: pipeline status

Clean old versions of Docker images.

Explanation
-----------

Remove old versions of images with same name. In cases where you updated an
image (from example from :code:`postgres:13` to :code:`postgres:14`) the old
image is present. Using :code:`docker image prune` won't help in this case
since the image is still properly tagged.

Usage
-----

.. code:: shell

    usage: deepclean [-h] [-i INCLUDE] [-e EXCLUDE] [-v] [-V] [-d]

    Clean old versions of Docker images.

    options:
      -h, --help            show this help message and exit
      -i INCLUDE, --include INCLUDE
                            Regular expression of images to exclusively prune.
      -e EXCLUDE, --exclude EXCLUDE
                            Regular expression of images to ignore.
      -v, --verbose         Verbose output
      -V, --version         show program's version number and exit
      -d, --dry-run         Dry-run, don't delete

    Regular Docker environment variables (like DOCKER_HOST) can be used.-i and -e can be used multiple times.

License
-------

This software is licensed under the MIT license (see the :code:`LICENSE.txt`
file).

Author
------

Nimrod Adar, `contact me <nimrod@shore.co.il>`_ or visit my `website
<https://www.shore.co.il/>`_. Patches are welcome via `git send-email
<http://git-scm.com/book/en/v2/Git-Commands-Email>`_. The repository is located
at: https://git.shore.co.il/nimrod/.
