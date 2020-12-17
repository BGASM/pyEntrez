# How to contribute


## Dependencies

We use [poetry](https://github.com/python-poetry/poetry) to manage the dependencies.
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
or  on windows powershell:
```bash
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```
Then within the cloned pyentrez root directory to install the dependencies you would need to run `install` command:

```bash
poetry install
```
Note, if you plan on developing any portion of the review screen or database interaction you will also need to add 
pymongo. (This is required even if you want to design sql interactions, as v.0.1.0 was designed with pymongo, and all 
basic hooks at this time require the pymongo library. Future releases we will make this more on-the-fly, so an SQL user 
won't need to install pymongo etc.)
```bash
poetry install -E pymongo
```

Then to activate your `virtualenv` run `poetry shell`. Now you should be able to run the script using `py pyentrez` 


## Tests

We use `pytest` and `flake8` for quality control.
We also use [wemake_python_styleguide](https://github.com/wemake-services/wemake-python-styleguide) to enforce the 
code quality.

To run all tests:

```bash
pytest
```

To run linting:

```bash
flake8 .
```
Keep in mind: default virtual environment folder excluded by flake8 style checking is `.venv`.
If you want to customize this parameter, you should do this in `setup.cfg`.
These steps are mandatory during the CI.


## Type checks

We use `mypy` to run type checks on our code.
To use it:

```bash
mypy src/pyentrez/.
```

This step is mandatory during the CI.


## Submitting your code

We use [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
development.

What the point of this method?

1. We use a protected `main` branch that represents the last working release. It only merges with `release` branches 
   (and occasionally `hotfix` branches.)
2. A `develop` branch from main will contain the complete, unabridged commit history of the project. When you clone 
   the repository, this is the branch that you should `track`.
3. All changes are done via `feature` branches checked-out from `develop`. You can make any changes you want on a 
   Feature-branch and push those branches onto the central repository. When your feature is complete, request a `pull` 
   back into `develop` so it can be reviewed and merged in.
4. When `develop` has enough features for a new release, a `release` branch is split from `develop`. At this point,
    no new features will be included in this release, only bugfixes, and documentation. Any features being worked on 
   after a release branch will be included in the next release.
5. Once all testing and fixes on `release` are complete it will be merged into `main` and back into `develop`

So, this way we achieve an easy and scalable development process
which frees us from merging hell and long-living branches.

In this method, the latest version of the app is always in the `main` branch.

### Before submitting

Before submitting your code please do the following steps:

1. Run `pytest` to make sure everything was working before
2. Add any changes you want
3. Add tests for the new changes
4. Edit documentation if you have changed something significant
5. Update `CHANGELOG.md` with a quick summary of your changes
6. Run `pytest` again to make sure it is still working
7. Run `mypy` to ensure that types are correct
8. Run `flake8` to ensure that style is correct
9. Run `doc8` to ensure that docs are correct


## Other help

You can contribute by spreading a word about this library.
It would also be a huge contribution to write
a short article on how you are using this project.
You can also share your best practices with us.
