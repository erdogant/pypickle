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


.. _security_mechanisms_save:

Security Mechanisms (save)
============================

There are various key security mechanisms implemented in the ``save()`` function to mitigate risks associated with saving pickle files, especially when allowing file writes outside predefined safe directories.
Before saving, the function performs several **security checks**:

- Ensures the filepath is located in user or temporary directories, unless overridden.
- Blocks writes to critical system paths.
- Accepts only known-safe extensions (``.pkl``, ``.pickle``, ``.pklz``, ``.pbz2``).
- Prevents directory traversal exploits like ``../../etc/passwd``.

The table below outlines how explicit user consent, robust path validation, prevention of path traversal exploits, and audit logging work together to protect the system from unauthorized or accidental overwrites.
   
   +-------------------------------+-------------------------------------------------------------+
   | Mechanism                     | Purpose                                                     |
   +===============================+=============================================================+
   | Internal (`cwd`, `tempdir`)   | Temp directories are permitted                              |
   +-------------------------------+-------------------------------------------------------------+
   | Home directory                | Home directory is permitted                                 |
   +-------------------------------+-------------------------------------------------------------+
   | ``allow_external=True``       | Explicit user opt-in to save outside safe directories       |
   +-------------------------------+-------------------------------------------------------------+
   | Critical path checks          | Prevents saving in system or protected paths                |
   +-------------------------------+-------------------------------------------------------------+
   | Extension validation          | Blocks non-pickle extensions (e.g., ``.exe``, ``.bat``)     |
   +-------------------------------+-------------------------------------------------------------+
   | Path traversal detection      | Detects and blocks path traversal attempts                  |
   +-------------------------------+-------------------------------------------------------------+
   | Audit logs                    | Logs warnings and overrides for traceability                |
   +-------------------------------+-------------------------------------------------------------+



.. code-block:: python

   import pypickle
   import tempfile
   import os

   # Safe save
   filepath = os.path.join(tempfile.gettempdir(), "test.pkl")
   data = [1, 2, 3, 4, 5]
   status = pypickle.save(filepath, data)

   # Allow external save
   filepath = "D:/myfolder/model.pkl"
   status = pypickle.save(filepath, data, allow_external=True)

   # Save with overwrite
   status = pypickle.save(filepath, data, allow_external=True, overwrite=True)

   # Unsafe extension (will be blocked)
   filepath = "C:/temp/script.bat"
   status = pypickle.save(filepath, data)




.. _critical_paths:

Critical System Paths
=====================

The following directories are considered *critical system paths* and are **blocked** from pickle saving to prevent security risks such as overwriting system files, tampering with user configurations, or compromising the operating system.

+-------------------------------------------+--------------------------------------------------------------+
| Path                                      | Description                                                  |
+===========================================+==============================================================+
| **UNIX**                                  |                                                              |
+-------------------------------------------+--------------------------------------------------------------+
| /bin, /boot, /dev, /etc, /lib, /lib64     | Core Unix/Linux system directories                           |
+-------------------------------------------+--------------------------------------------------------------+
| /proc, /root, /sbin, /sys, /usr, /var     | Additional system-critical paths on Unix/Linux               |
+-------------------------------------------+--------------------------------------------------------------+
| ~/.ssh                                    | Contains SSH private keys and credentials                    |
+-------------------------------------------+--------------------------------------------------------------+
| ~/.gnupg                                  | Contains GPG encryption keys and configuration               |
+-------------------------------------------+--------------------------------------------------------------+
| ~/.config                                 | User configuration files                                     |
+-------------------------------------------+--------------------------------------------------------------+
| ~/.local/share                            | User application data and caches                             |
+-------------------------------------------+--------------------------------------------------------------+
| **MACOS**                                 |                                                              |
+-------------------------------------------+--------------------------------------------------------------+
| /System, /Library, /Network               | macOS system directories                                     |
+-------------------------------------------+--------------------------------------------------------------+
| /private                                  | macOS directory for system-level files (e.g., /etc, /var)    |
+-------------------------------------------+--------------------------------------------------------------+
| /Volumes                                  | macOS mounted volumes                                        |
+-------------------------------------------+--------------------------------------------------------------+
| /Applications                             | macOS applications                                           |
+-------------------------------------------+--------------------------------------------------------------+
| /usr/local/bin                            | macOS Homebrew and CLI tool location                         |
+-------------------------------------------+--------------------------------------------------------------+
| **WINDOWS**                               |                                                              |
+-------------------------------------------+--------------------------------------------------------------+
| C:\Windows, C:\Windows\System32           | Core Windows system files                                    |
+-------------------------------------------+--------------------------------------------------------------+
| C:\Program Files, C:\Program Files (x86)  | Installed Windows applications                               |
+-------------------------------------------+--------------------------------------------------------------+
| C:\ProgramData, C:\Recovery               | Windows system and recovery data                             |
+-------------------------------------------+--------------------------------------------------------------+
| %APPDATA%                                 | Windows per-user application data (e.g., config, cache)      |
+-------------------------------------------+--------------------------------------------------------------+
| %LOCALAPPDATA%                            | Windows local application data                               |
+-------------------------------------------+--------------------------------------------------------------+

.. code-block:: python

   import pypickle
   import os

   # Check for critical path
   status = pypickle.is_critical_path(r'/tmp')
   pypickle.is_critical_path("C:\\Users\\User\\AppData\\Local\\Temp\\myfile.pkl")
   False
   
   pypickle.is_critical_path("C:\\Windows\\System32\\config.sys")
   True

.. code-block:: python

   # Get all critical paths
   crit_paths = pypickle.get_critical_paths()
   print(crit_paths)

    # ['/bin',
    #  '/boot',
    #  '/dev',
    #  '/etc',
    #  '/lib',
    #  '/lib64',
    #  '/proc',
    #  '/root',
    #  '/sbin',
    #  '/sys',
    #  '/usr',
    #  '/var',
    #  'C:\\Users\\username/.ssh',
    #  'C:\\Users\\username/.gnupg',
    #  'C:\\Users\\username/.config',
    #  'C:\\Users\\username/.local/share',
    #  '/System',
    #  '/Library',
    #  '/Network',
    #  '/private',
    #  '/Volumes',
    #  '/Applications',
    #  '/usr/local/bin',
    #  'C:\\Windows',
    #  'C:\\Windows\\System32',
    #  'C:\\Program Files',
    #  'C:\\Program Files (x86)',
    #  'C:\\ProgramData',
    #  'C:\\Recovery',
    #  'C:\\Users\\username\\AppData\\Roaming',
    #  'C:\\Users\\username\\AppData\\Local']


.. note::

   Attempts to save pickle files into these directories will be blocked, unless explicitly overridden (not recommended).


.. code-block:: python

   import pypickle
   import tempfile
   import os

   # Safe save
   filepath = os.path.join(tempfile.gettempdir(), "test.pkl")
   data = [1, 2, 3, 4, 5]
   status = pypickle.save(filepath, data)

   # Critical system path (will be blocked)
   filepath = "/etc/"
   status = pypickle.save(filepath, data, overwrite=True)
   # [pypickle.pypickle] [WARNING] [BLOCKED]: Extention must be of type ['.pkl', '.pickle', '.pklz', '.pbz2']: [/etc/] is not allowed.

   # Critical system path (will be blocked)
   filepath = "/etc/test.pkl"
   status = pypickle.save(filepath, data, overwrite=True)
   # [pypickle.pypickle] [WARNING] [BLOCKED]: Filepath: [/etc/test.pkl] is under critical path: [/etc]

   # Critical system path (will be blocked)
   filepath = "/etc/test.pkl"
   status = pypickle.save(filepath, data, overwrite=True, allow_external=True)
   # [pypickle.pypickle] [WARNING] [BLOCKED]: Filepath: [/etc/test.pkl] is under critical path: [/etc]




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