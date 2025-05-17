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

+------------------------+----------+-------------------------------------------------------------+
| Module Type            | Allowed? | How to Change Behavior                                      |
+========================+==========+=============================================================+
| Default safe           | ✅       | Always allowed                                              |
+------------------------+----------+-------------------------------------------------------------+
| Risky (``os``, etc.)   | ❌       | Must be explicitly added via ``validate=['os']``            |
+------------------------+----------+-------------------------------------------------------------+
| Custom safe            | ✅       | If included in ``validate`` param                           |
+------------------------+----------+-------------------------------------------------------------+
| Unknown                | ✅       | Allowed unless in risky list                                |
+------------------------+----------+-------------------------------------------------------------+


Save
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


Save - with Validation
------------------------

To avoid exploits when loading pickle files, only built-in modules can be safely loaded. However, the ``validate`` parameter allows to load modules that
you can mark as ``safe``. See below an example where we can save a ``sklearn`` model, and load it safely where we include the expected validation.

.. code:: python

    from sklearn.linear_model import LogisticRegression
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    import pypickle
    
    # Load example dataset
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    
    # Train a model
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Save the model
    pypickle.save('model.pkl', model, overwrite=True)
    
    # Load the model but without adding validate safe=False because sklearn models use custom classes)
    model_loaded = pypickle.load('model.pkl', validate=False)
    
    # Predict
    predictions = model_loaded.predict(X_test)
    print(predictions)


Load
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