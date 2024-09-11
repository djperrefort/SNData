Quick Start
===========

The following is provided as a short example on how to import a supernova
data release, download the corresponding data, and read it into memory.
For a more in depth overview, see the :ref:`SlowStart`.

.. code-block:: python
   :linenos:

   # All data releases are available as ``sndata.<survey name>.<release name>``
   from sndata.csp import DR3

   # Start by creating an instance of the data release
   dr3 = DR3()

   # Use ``help`` to get a description of the survey
   print(help(dr3))

   # Download data to your machine.
   # Note: If data is already downloaded, this function call won't do anything.
   dr3.download_module_data()

   # Check what tables are available from the release's corresponding publication
   published_tables = dr3.get_available_tables()
   print(published_tables)

   # Read one of those tables by referencing the table name or number
   dr3_demo_table = dr3.load_table(published_tables[0])

   # Check what objects are included in the data release
   object_ids = dr3.get_available_ids()
   print(object_ids)

   # Read in the data for an object using it's Id
   demo_id = object_ids[0]
   dr3.get_data_for_id(demo_id)

   # Data is auto-formatted to be compatible with the SNCosmo package.
   # To disable this and return data as presented on the data release,
   # set ``format_table=False``.
   dr3.get_data_for_id(demo_id, format_table=False)

   # For convenience you can iterate over all tables
   data_iterator = dr3.iter_data()
   for data in data_iterator:
       print('The first data table:')
       print(data)
       break
