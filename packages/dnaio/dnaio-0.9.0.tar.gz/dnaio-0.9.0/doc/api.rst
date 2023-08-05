The dnaio API
=============


.. module:: dnaio

The open function
-----------------

.. autofunction:: open


The ``SequenceRecord`` class
------------------------------

.. autoclass:: dnaio.SequenceRecord
   :members:
   :special-members: __len__, __getitem__

   .. automethod:: __init__(name: str, sequence: str, qualities: Optional[str] = None)


Reader and writer classes
-------------------------

.. autoclass:: FastaReader

.. autoclass:: FastaWriter
   :members: write

.. autoclass:: FastqReader

.. autoclass:: FastqWriter
   :members: writeseq

   .. py:method:: write(record: SequenceRecord) -> None:

      Write a SequenceRecord to the FASTQ file.

.. autoclass:: TwoFilePairedEndReader

.. autoclass:: TwoFilePairedEndWriter

.. autoclass:: InterleavedPairedEndReader

.. autoclass:: InterleavedPairedEndWriter
   :members: write

.. autoclass:: SingleEndReader

.. autoclass:: PairedEndReader

.. autoclass:: SingleEndWriter

.. autoclass:: PairedEndWriter
   :members: write


Chunked reading of sequence records
-----------------------------------

The following functions can be used to very quickly split up the input file(s)
into similarly-sized chunks without actually parsing the records. The chunks
can then be distributed to worker threads or subprocesses and be parsed and
processed there.

.. autofunction:: read_chunks
.. autofunction:: read_paired_chunks


Exceptions
----------

.. autoexception:: UnknownFileFormat

.. autoexception:: FileFormatError

.. autoexception:: FastaFormatError
   :show-inheritance:

.. autoexception:: FastqFormatError
   :show-inheritance:
