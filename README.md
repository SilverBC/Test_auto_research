# Comparison of Programming Languages for Test Automation

This project is a part of a research paper intended to compare five
different programming languages as they perform the same test cases
using the Selenium web testing framework.

The paper can be viewed here: *TODO: link to the paper.*

# Structure of the repository

Below is a high-level overview of the project's structure.

```
/ (root)
| Pipfile                    - Used to configure both the python tests and
| Pipfile.lock                 the custom launcher script
| pom.xml                    - Used to configure the java tests, though the
|                              source code lives elsewhere.
| telemetry.py               - The custom test launcher script.
|
| src                        - Contains the source code for automated tests.
|--test
|----C#                      - Also contains the C# project definition.
|----java
|----JavaScript              - Also contains package.json.
|----python
|----Ruby                    - Also contains the Gemfile.
```

# Running the tests

**Attention**: for all of the instructions to work properly (except
Java and Python), you need to be located in the chosen language's
source directory. For example, before running the ruby project, make
sure to go into the `src/test/Ruby` directory.

## Java

For this test to work, you need to be at the project's root directory.
Ensure that [maven](https://maven.apache.org/) is installed in your
system.

If you want to always compile first, run:

```
mvn clean test
```

Otherwise:

```
mvn test
```

## C#

First, install the .NET core SDK. On ubuntu, this can be done with:

```
sudo apt-get update && sudo apt-get install -y dotnet-sdk-7.0
```

After that, run the test via:

```
dotnet test
```

## JavaScript

Ensure that [node.js](https://nodejs.org/en) is installed in your
system. Go to `src/test/JavaScript`, then run:

```
npm install
```

Afterwards, run the test with:

```
npm test
```

## Python

Ensure that python and [pipenv](https://pypi.org/project/pipenv/) are
installed on your system. Then, install the dependencies via:

```
pipenv install
```

Afterwards, run the test with:

```
pipenv run pytest src/test/python/CommerceTest.py
```

## Ruby

Ensure that ruby is installed in your system. Then, Go to
`src/test/Ruby` and install all dependencies via:

```
bundle install
```

Afterwards, run the test with:

```
ruby CommerceTest.rb
```

