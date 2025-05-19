What is pickling?
###########################

Pickling is useful for applications where you need some degree of persistency in your data. Your program's state data can be saved to disk, so you can continue working on it later on. It can also be very useful when you're working with machine learning algorithms, where you want to save them to be able to make new predictions at a later time, without having to rewrite everything or train the model all over again [1]. Note that pickling does not involve any compression.


Data Modules
###########################

You can ``pypickle`` the underneath data types but it is also possible to pickle classes and functions.
Not everything can be pickled, Examples that can not be pickled are ``generators``, ``inner classes``, ``lambda`` functions and ``defaultdicts`` and saving machine learning models can also be troublesome.
In the case of lambda functions, you need to use an additional package named dill. With defaultdicts, you need to create them with a module-level function.
Examples of modules that can be saved are:

	* Booleans
	* Integers
	* Floats
	* Complex numbers
	* Strings (normal and Unicode)
	* Tuples
	* Lists
	* Sets
	* Dictionaries that ontain picklable objects.



.. include:: add_bottom.add