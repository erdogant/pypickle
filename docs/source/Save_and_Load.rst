What is pickling?
###########################

Pickling is useful for applications where you need some degree of persistency in your data. Your program's state data can be saved to disk, so you can continue working on it later on. It can also be very useful when you're working with machine learning algorithms, where you want to save them to be able to make new predictions at a later time, without having to rewrite everything or train the model all over again [1]. Note that pickling does not involve any compression.


Data Modules
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

+------------------------+----------+------------------------------------------------------------------------+
| Module Type            | Allowed? | How to Change Behavior                                                 |
+========================+==========+========================================================================+
| Unknown                | ✅       | Allowed unless in risky list                                           |
+------------------------+----------+------------------------------------------------------------------------+
| Risky (``os``, etc.)   | ❌       | Must be explicitly added via ``validate=['nt']`` or ``validate=False`` |
+------------------------+----------+------------------------------------------------------------------------+
| Custom safe            | ✅       | If included in ``validate`` param                                      |
+------------------------+----------+------------------------------------------------------------------------+


Risk Modules
#############
.. list-table:: Risky Modules Blocked by Default
   :widths: 20 80
   :header-rows: 1

   * - Module
     - Risk / Reason for Blocking
   * - os
     - Shell access, file system, environment
   * - subprocess
     - Can execute arbitrary system commands
   * - sys
     - System-level operations, e.g., path, exit
   * - nt
     - Windows native system calls (like os)
   * - posix
     - Unix equivalent of nt
   * - builtins
     - If abused (e.g., eval, exec); handled separately
   * - importlib
     - Dynamic importing
   * - socket
     - Network access
   * - selectors
     - Low-level network/socket
   * - multiprocessing
     - Starts subprocesses
   * - threading
     - Concurrency (can spawn dangerous threads)
   * - asyncio
     - Async tasks (can be misused)
   * - ctypes
     - Can load arbitrary C libraries
   * - platform
     - Access system info
   * - webbrowser
     - Can open URLs or trigger browser actions
   * - shutil
     - File operations, disk wiping
   * - tempfile
     - File system operations
   * - glob
     - Can access wildcards over filesystem
   * - pathlib
     - File access (safe in limited form, but still risky)
   * - codecs
     - Can decode to arbitrary formats (rare exploit)


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


Modules
------------------------

To avoid exploits when loading pickle files we can use the ``validate`` parameter that allows to load modules that you can mark as ``safe``.
See below an example where we can save a ``sklearn`` model, and load it safely where we include the expected modules.

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
    status = pypickle.save('model.pkl', model, overwrite=True)

    # Gather the modules which you can use later to load the pickle file with the expected modules.
    mods = pypickle.validate_modules('model.pkl')
    # ['classes_',
    #  'numpy',
    #  'numpy._core.multiarray',
    #  'sklearn.linear_model._logistic']
    model_loaded = pypickle.load('model.pkl', validate=mods)
    
    # Load the model but without adding ``validate=False``)
    model_loaded = pypickle.load('model.pkl', validate=False)
    
    # Predict
    predictions = model_loaded.predict(X_test)
    print(predictions)


Brute-force
------------------------

All pickle files can be loaded using ``validate=False`` parameter. This will ignore all module types and risk classifications.
See below an example how pypickle can not load an exploit but requires to use a validation or brute-force loading.

.. code:: python

    # Create a malicious pickle trying to execute code (like opening calculator)
    class Exploit:
        def __reduce__(self):
            import os
            return (os.system, ("echo 'Exploit executed'",))
    
    import pypickle
    filepath = 'malicious.pkl'
    pypickle.save(filepath, Exploit(), overwrite=True)
    
    # Attempt safe load
    loaded = pypickle.load(filepath)

    # Brute-force load and ignore all risk modules
    loaded = pypickle.load(filepath, validate=False)

    # Load using validation
    mods = pypickle.validate_modules(filepath)
    # Load
    loaded = pypickle.load(filepath, validate=mods)



[1] https://www.datacamp.com/community/tutorials/pickle-python-tutorial


.. include:: add_bottom.add