# Comparison of Programming Languages for Test Automation

This project is a part of a research paper intended to compare five
different programming languages as they perform the same test case
using the Selenium web testing framework.

The test case is as follows:

1. Go to https://www.saucedemo.com
2. Log in with the standard user (details about this can be found on
the login page)
3. Click on the "Add to Cart" button of the Sauce Labs Backpack item
card
4. Go to the shopping cart
5. Check that the name of the item displayed on the Cart page is "Sauce
   Labs Backpack"
6. Press the Checkout button
7. In the following screen, enter "John" as the first name
8. Enter "Doe" as the last name
9. Enter "10001" as the ZIP/Postal code.
10. Press the Continue button
11. Check that the name of the item displayed on the Checkout page is
    "Sauce Labs Backpack"
12. Press the Finish button
13. Validate that the success screen is visible.

# Running the tests

Disclaimer: for all of the instructions to work properly (except
Java), you need to be in the relevant directory. For example, before
running the python project, make sure to go into the `src/test/python`
directory.

## Java

For this test to work, you need to be at the project's root directory.

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

Go to `src/test/JavaScript`, then run:

```
npm install
```

Afterwards, run the test with:

```
npm test
```

## Python

Assuming `requests` and `selenium` libraries are installed, run:

```
python CommerceTest.py
```

## Ruby

Run:

Assuming the `selenium-webdriver` and `test-unit` gems are installed, run:

```
ruby CommerceTest.rb
```

