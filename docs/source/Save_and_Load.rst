.. include:: add_top.add

What is pickling?
###########################

Pickling is useful for applications where you need some degree of persistency in your data. Your program's state data can be saved to disk, so you can continue working on it later on. It can also be very useful when you're working with machine learning algorithms, where you want to save them to be able to make new predictions at a later time, without having to rewrite everything or train the model all over again [1]. Note that pickling does not involve any compression.


Store types of data
###########################

You can ``pypickle`` the underneath data types but it is also possible to pickle classes and functions.

	* Booleans
	* Integers
	* Floats
	* Complex numbers
	* Strings (normal and Unicode)
	* Tuples
	* Lists
	* Sets
	* Dictionaries that ontain picklable objects.


Not everything can be pickled (easily), though: examples of this are generators, inner classes, lambda functions and defaultdicts. In the case of lambda functions, you need to use an additional package named dill. With defaultdicts, you need to create them with a module-level function.

Saving
#########

The pypickle module serializes objects so they can be saved to a file, and loaded in a program again later on.
There are many types that can be saved, such as dictionaries, DataFrames, lists, etc. Saving can be performed using :func:`pypickle.pypickle.save`:

.. code:: python

	import pypickle
	filepath = 'test.pkl'

	# Some data in a list
	data = [1,2,3,4,5]

	# Save
	status = pypickle.save(filepath, data)



Loading
#########

Loading a pickled file can performed using the function :func:`pypickle.pypickle.load`:

.. code:: python

	import pypickle
	filepath = 'test.pkl'

	# Some data in a list
	data = [1,2,3,4,5]

	# Save
	status = pypickle.save(filepath, data)

	# Load file
	data = pypickle.load(filepath)



[1] https://www.datacamp.com/community/tutorials/pickle-python-tutorial




.. include:: add_bottom.add