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




.. include:: add_bottom.add