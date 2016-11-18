===========================================
Ptolemy, an AWS DMS table mapping generator
===========================================

Write terse AWS DMS table mappings.


Background
----------

Amazon Web Services provides a tool for migrating data to, from or between SQL databases. This tool is named `Database Migration Service <https://aws.amazon.com/documentation/dms/>`_ (DMS). When running DMS, users can supply a table mapping, which specifies allows the user to control what data is sent from the source database to the target database. A full list of table mapping options can be found `here <http://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TableMapping.html>`_.

Table mappings are written as JSON documents, which can grow to be long and complex. ``ptolemy`` allows the user to write terse YAML ``source`` files, which can be compiled to valid JSON table mappings using the ``ptolemy`` cli tool.


Usage
-----

.. code-block:: console

  $ # Display an example source file:
  $ cat migrate_all_tables_in_a_schema.yaml
  selection:
    include:
      -
        object-locators:
          schema-names:
            - Test
          table-names:
            - "%"
  $ # Compile it to a DMS table mapping:
  $ ptolemy migrate_all_tables_in_a_schema.yaml
  {
      "rules": [
          {
              "object-locator": {
                  "schema-name": "Test",
                  "table-name": "%"
              },
              "rule-action": "include",
              "rule-id": "1",
              "rule-name": "1",
              "rule-type": "selection"
          }
      ]
  }


API
---

.. code-block:: console

  $ ptolemy -h
  ptolemy [-h] [-d] [-v] source

  positional arguments:
    source         path to the source file

  optional arguments:
    -h, --help     show this help message and exit
    -d, --debug    enable debug logs
    -v, --version  show program's version number and exit


Install
-------

Install via pip (recommended):

.. code-block:: console

  $ pip install ptolemy

Install from source:

.. code-block:: console

  $ git clone git@github.com:cloudreach/ptolemy.git
  $ cd ptolemy
  $ make install


License
-------

ptolemy is licensed under the Apache Software License 2.0.


Source Syntax
-------------

The following sections describe the source syntax. It is intended to show users who have working knowledge of DMS JSON mapping files how to write their YAML equivalents. For an overview of the JSON mapping files, see the `documentation <http://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TableMapping.html>`_. Most items are the same as those in JSON mapping files, with the exception of ``object-locators``, which are explained in the section `Object Locators`_

The descriptions are written in pseudo-yaml, where the syntax ``( option_a|option_b )`` indicates that an item could take the value ``option_a`` or ``option_b``.

For working examples, see the `examples directory <https://github.com/cloudreach/ptolemy/tree/master/examples>`_.


Selection Rules and Actions
***************************

.. code-block:: YAML

  selection:
    ( include|exclude ):
      -
        object-locators:
          schema-names:
            - <schema-name-1>
          table-names:
            - <table-name-1>
          filters:
            -
              filter-type: source
              column-name: <column-name-1>
              filter-conditions:
                -
                  filter-operator: ( ste|gte|eq|between )
                  value: <value>


Transformation Rules and Actions
********************************

.. code-block:: YAML

  transformation:
    ( rename|remove-column|convert-lowercase|convert-uppercase|add-prefix|remove-prefix|replace-prefix|add-suffix|remove-suffix|replace-suffix ):
      -
        object-locators:
          schema-names:
            - <schema-name-1>
          table-names:
            - <table-name-1>
          column-names:
            - <column-name-1>
        rule-target: ( schema|table|column )
        value: <value>
        old-value: <old-value>


Object Locators
***************

``object-locators`` offer a powerful way to apply selection and transformation rules to large numbers of objects. The singular ``schema-name``, ``table-name`` and ``column-name`` parameters of the native JSON table mapping ``object-locator`` have been replaced by their plurals. These new parameters each accept a list of objects. The rule is then applied to each column listed, for each table listed, for each schema listed.


Multiple Source File Compilation
--------------------------------

Multiple source files can be compiled at once with the following Bash snippet. The snippet recursively finds all YAML files under the directory ``src/``, compiles the source to a DMS mapping file, and saves it to a file with the same name and path under a directory named ``mappings/``, with the extension ``.json``.

.. code-block:: bash

  source_files="$(find src -type f -name '*.yaml')"
  for source_file in $source_files; do
    source_file_without_extension=${source_file%.*}
    source_file_with_json_extension=${source_file_without_extension}.json
    destination_file=mappings${source_file_with_json_extension#src}
    mkdir -p "$(dirname $destination_file)"
    ptolemy $source_file > $destination_file
  done

Running the code from the following directory:

.. code-block:: console

  .
  └── src
    ├── db-a
    │   ├── schema-1.yaml
    │   └── schema-2.yaml
    └── db-b
        ├── schema-1.yaml
        └── schema-2.yaml

would result in:

.. code-block:: console

  .
  ├── mappings
  │   ├── db-a
  │   │   ├── schema-1.json
  │   │   └── schema-2.json
  │   └── db-b
  │       ├── schema-1.json
  │       └── schema-2.json
  └── src
      ├── db-a
      │   ├── schema-1.yaml
      │   └── schema-2.yaml
      └── db-b
          ├── schema-1.yaml
          └── schema-2.yaml
