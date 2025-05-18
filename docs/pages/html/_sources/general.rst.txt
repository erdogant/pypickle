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

Risk modules refer to Python modules that, when deserialized using ``pickle``, may execute unintended or harmful code due to their built-in capabilities.
Modules such as ``os``, ``subprocess``, ``sys``, or custom classes with overridden ``__reduce__`` or ``__setstate__`` methods can introduce severe security risks during unpickling.
These modules are often classified as *high-risk* because they enable file system access, process execution, or system-level interactions.
To mitigate these threats, ``pypickle`` includes validation mechanisms that block or explicitly require user approval for such modules before loading, ensuring safer handling of untrusted pickle files.


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


.. include:: add_bottom.add