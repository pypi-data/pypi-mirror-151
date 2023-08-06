# Ping Payments Python SDK

[![Tests](https://github.com/youcal/ping_python_sdk/actions/workflows/tests.yml/badge.svg)](https://github.com/youcal/ping_python_sdk/actions/workflows/tests.yml)
[![PyPI version](https://badge.fury.io/py/ping-sdk.svg)](https://badge.fury.io/py/ping-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Use this Python library to manage Ping Payments API regarding merchants, payment orders, payments and payouts.

## Table of contents

-   [Requirements](#requirements)

-   [Installation](#installation)

-   [Payments API](#payments-api)

## Requirements

The SDK supports the following versions of Python:

-   Python 3 versions 3.7 and later

## Installation

Install the latest SDK using pip:

```sh
pip install ping-sdk
```

## Payments API

### [Payments API]

-   [Merchant]

-   [Payment Orders]

-   [Payment]

-   [Payout]

-   [Ping]

### Usage

First time using Payments API? Here’s how to get started:

#### Get a tenant ID

To use the Payments API to manage the resources you need to get a tenant ID. A tenant ID is provided to you by Ping Payments.

When you call the Payments API, you call it using a tenant ID. A tenant ID has specific permissions to resources.
**Important:** Make sure you store and access the tenant ID securely.

To use the Payments API, you import the PaymentsAPI class, instantiate a PaymentsAPI object, and initialize it with the appropriate tenant ID and environment. Here’s how:

1. Import the PaymentsApi class from the Ping Python SDK module so you can call the Payments API:

```python

from ping.payments_api import PaymentsApi

```

2. Instantiate a PaymentsApi object and initialize it with the tenant ID and the environment that you want to use.

To access sandbox resources, initialize the PaymentsApi with environment set to sandbox:

```python

payments_api = PaymentsApi(
		tenant_id = '55555555-5555-5555-5555-555555555555',
		environment = 'sandbox'
)

```

To access production resources, initialize the PaymentsApi with environment set to production:

```python

payments_api = PaymentsApi(
		tenant_id = '55555555-5555-5555-5555-555555555555',
		environment = 'production'
)

```

To test the API connection you can ping it. If a connection is established it will return `pong`.

```python

payments_api.ping.ping_the_api()

```

#### Get an Instance of an API object and call its methods

The API is implemented as a class. With the PaymentsApi object you work with an API by calling it's methods.

**Work with the API by calling the methods on the API object.** For example, you would call get_merchants to get a list of all merchant for the tenant:

```python

result = payments_api.merchant.get_merchants()

```

See the SDK documentation for the list of methods for the API class.

#### Handle the response

API calls return an ApiResponse object that contains properties that describe both the request (headers and request) and the response (status_code, reason_phrase, text, errors, body, and cursor). Here’s how to handle the response:

**Check whether the response succeeded or failed.** ApiResponse has two helper methods that enable you to easily determine the success or failure of a call:

```python

if result.is_success():
	# Display the response as text
	print(result.text)
# Call the error method to see if the call failed
elif result.is_error():
	print(f"Errors: {result.errors}")

```

[//]: # "Link anchor definitions"
[payments api]: doc/payments_api.md
[merchant]: doc/api_resources/payments_api/merchant.md
[payment orders]: doc/api_resources/payments_api/paymentOrder.md
[payment]: doc/api_resources/payments_api/payment.md
[payout]: doc/api_resources/payments_api/payout.md
[ping]: doc/api_resources/payments_api/ping.md
