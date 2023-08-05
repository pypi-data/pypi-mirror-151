# python-ekp-sdk

This sdk is used to create frontend components like div, span, columns, rows, datatable and etc., for python modules.
Number of components will increase in the future.

Developed by **Earn Keeper** team (c)

# Developing Locally

First, you should have setuptools to be installed into your environment <br>
```pip install setuptools```

Then, if you made changes into the SDK by adding new module into it, you should add its name to **top_level_imports** file <br>

If you used some additional package in SDK that is not listed in **requirements.txt** file, you should add its name and version in specified format into this file.


After making changes into SDK, you should use the following command, which will build some wheel files, which will allow you to install and import it locally <br>
```python setup.py bdist_wheel```

In order to install it locally, type following command: <br>
```pip install -e .```

After successful installation, you can now open python console for testing using **python** command, and import any module, for example <br>
```from sdk import components ```

And if no error occurs, it means that testing went successfully 
and you can use it now

# Deploying

Now when you have tested package locally, to push it into pip, you should use twine tool.
First install it using ```pip install twine``` command <br>

Then, if you have updated SDK with additional files, you should add it into the 

**Note: Don't forget to update your release version in the VERSION variable of setup.py file, otherwise it will throw an error, because pip requires version updating for each release**

Now run this command, which will build the **tar** file, which will be uploaded to PyPi <br>
```python setup.py sdist```

After running command above, you will see tar file appeared in dist directory. To check if all the necessary sources and components of our project is in this tar file, run the following command: <br>
```tar tzf dist/<tar_file_name>```

Now after building the final structure and ready to deploy, run the following command: <br>
```twine upload dist/*```

It will ask for username and password of PyPi account. After typing them, you will get the success mesage within the link to your project in PyPi.
