Load
#########

A pickle file is loaded using the function :func:`pypickle.pypickle.load`.
Because of security reasons, that are various restrictions for loading.



.. _security_mechanisms_load:

Security Mechanisms (load)
===========================
pickle files are directly loaded if all modules are in the allowlist. If the pickle file contains unknown modules, the modules needs to be validated using the validate parameter.
pickle files that contain risky modules, i.e., those that can automatically make changes on the system or start (unwanted) applications are not allowed unless specifically specified using the validate parameter.


+---------------------------------+----------+------------------------------------------------------------------------+
| Module Type                     | Allowed? | How to Change Behavior                                                 |
+=================================+==========+========================================================================+
| Unknown                         | ✅       | Allowed unless in risky list                                           |
+---------------------------------+----------+------------------------------------------------------------------------+
| Risk modules (``os``, etc.)     | ❌       | No risk modules can be loaded unless exlicitely stated                 |
+---------------------------------+----------+------------------------------------------------------------------------+
| Risky modules  (``os``, etc.)   | ✅       | Must be explicitly added via ``validate=['nt']`` or ``validate=False`` |
+---------------------------------+----------+------------------------------------------------------------------------+


.. code:: python

	import pypickle
	filepath = 'test.pkl'

	# Some data in a list
	data = [1,2,3,4,5]

	# Save
	status = pypickle.save(filepath, data)

	# Load file
	data = pypickle.load(filepath)


Load with Validation
=====================

To prevent exploits when loading pickle files, use the ``validate`` parameter to explicitly allow only trusted modules. This ensures that only known-safe objects are deserialized.
For example, you can safely load any pickled module such as ``sklearn`` by specifying the expected modules as allowed. See the example below for how to use this mechanism securely.

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


Load without Validation
=========================

All pickle files can be loaded by setting the ``validate=False`` parameter. This disables all module and risk validation checks, allowing any object to be deserialized—including potentially unsafe ones.
Below is an example where ``pypickle`` refuses to load a known exploit unless validation is explicitly bypassed. While disabling validation is possible, **it is strongly discouraged unless you fully trust the source**.

.. code:: python

    # Create a pickle that can perform risky operations.
    class risky_module:
        def __reduce__(self):
            import os
            return (os.system, ("echo 'Unsafe action executed'",))
    
    import pypickle
    filepath = 'risky_module.pkl'
    pypickle.save(filepath, risky_module(), overwrite=True)
    
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