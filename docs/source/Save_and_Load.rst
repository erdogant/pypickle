What is pickling?
###########################

Pickling is useful for applications where you need some degree of persistency in your data. Your program's state data can be saved to disk, so you can continue working on it later on. It can also be very useful when you're working with machine learning algorithms, where you want to save them to be able to make new predictions at a later time, without having to rewrite everything or train the model all over again [1]. Note that pickling does not involve any compression.


Store types of data
###########################

You can ``ismember`` the underneath data types but it is also possible to pickle classes and functions.

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

The ismember module serializes objects so they can be saved to a file, and loaded in a program again later on.
There are many types that can be saved, such as dictionaries, DataFrames, lists, etc. Saving can be performed using :func:`ismember.ismember.save`:

.. code:: python

	import ismember
	filepath = 'test.pkl'

	# Some data in a list
	data = [1,2,3,4,5]

	# Save
	status = ismember.save(filepath, data)



Loading
#########

Loading a pickled file can performed using the function :func:`ismember.ismember.load`:

.. code:: python

	import ismember
	filepath = 'test.pkl'

	# Some data in a list
	data = [1,2,3,4,5]

	# Save
	status = ismember.save(filepath, data)

	# Load file
	data = ismember.load(filepath)



[1] https://www.datacamp.com/community/tutorials/pickle-python-tutorial


.. raw:: html

	<hr>
	<center>
		<script async type="text/javascript" src="//cdn.carbonads.com/carbon.js?serve=CEADP27U&placement=erdogantgithubio" id="_carbonads_js"></script>
	</center>
	<hr>
