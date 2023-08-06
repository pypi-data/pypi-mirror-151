# PDX-lib

A library of functions to help speed up common development tasks at PSU


### Installing Locally (development/testing)
1. `python setup.py sdist bdist_wheel --universal`
2. `pip install dist/pdx-X.X.X-py2.py3-none-any.whl --force-reinstall`


### Publishing to PyPi
1. Create accounts on [PyPi](https://pypi.org/account/register/) and [Test PyPi](https://test.pypi.org/account/register/)
2. Create `~/.pypirc`
    ```
    [distutils]
    index-servers=
        pypi
        testpypi
    
    [testpypi]
    repository: https://test.pypi.org/legacy/
    username: mikegostomski
    password: pa$$w0rd
    
    [pypi]
    username: mikegostomski
    password: pa$$w0rd
    ```
3. Ask an existing developer to add you as a collaborator - 
[test](https://test.pypi.org/manage/project/pdx-lib/collaboration/) and/or 
[prod](https://pypi.org/manage/project/pdx-lib/collaboration/)
4. `python setup.py sdist bdist_wheel --universal`
5. `twine upload --repository testpypi dist/*`
6. `twine upload dist/*`
7. Tag the release in Git.  Don't forget to push the tag!
Example:
```shell script
git tag 0.1.2
git push origin 0.1.2 
```