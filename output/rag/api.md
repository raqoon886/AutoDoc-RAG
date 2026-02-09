**requests.api**
================

This module implements the Requests API. It provides a high-level interface for making HTTP requests in Python.

### Module Overview

The `requests` library is designed to be easy to use and intuitive. It follows the architectural concept of the D-Bus protocol, which emphasizes simplicity and ease of use. The library uses a session-based approach, where each request is associated with a session object that manages the underlying connection.

### Classes/Structs

#### None

There are no classes or structs defined in this module.

### Functions

#### `request(method, url, **kwargs)`

Constructs and sends a :class:`Request <Request>`.

*   **Signature:** `def request(method, url, **kwargs)`
*   **Description:** This function constructs and sends a :class:`Request <Request>`. It takes the method for the new :class:`Request` object, the URL for the new :class:`Request` object, and optional keyword arguments.
*   **Parameters:**
    *   `method`: The method for the new :class:`Request` object. Can be one of ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
    *   `url`: The URL for the new :class:`Request` object.
    *   `**kwargs`: Optional keyword arguments that can be passed to the function.
*   **Return Value:** A :class:`Response <Response>` object.

#### `get(url, params=None, **kwargs)`

Sends a GET request.

*   **Signature:** `def get(url, params=None, **kwargs)`
*   **Description:** This function sends a GET request. It takes the URL for the new :class:`Request` object and optional keyword arguments.
*   **Parameters:**
    *   `url`: The URL for the new :class:`Request` object.
    *   `params`: (optional) Dictionary, list of tuples or bytes to send in the query string for the :class:`Request`.
    *   `**kwargs`: Optional keyword arguments that can be passed to the function.
*   **Return Value:** A :class:`Response <Response>` object.

#### `options(url, **kwargs)`

Sends an OPTIONS request.

*   **Signature:** `def options(url, **kwargs)`
*   **Description:** This function sends an OPTIONS request. It takes the URL for the new :class:`Request` object and optional keyword arguments.
*   **Parameters:**
    *   `url`: The URL for the new :class:`Request` object.
    *   `**kwargs`: Optional keyword arguments that can be passed to the function.
*   **Return Value:** A :class:`Response <Response>` object.

#### `head(url, **kwargs)`

Sends a HEAD request.

*   **Signature:** `def head(url, **kwargs)`
*   **Description:** This function sends a HEAD request. It takes the URL for the new :class:`Request` object and optional keyword arguments.
*   **Parameters:**
    *   `url`: The URL for the new :class:`Request` object.
    *   `**kwargs`: Optional keyword arguments that can be passed to the function.
*   **Return Value:** A :class:`Response <Response>` object.

#### `post(url, data=None, json=None, **kwargs)`

Sends a POST request.

*   **Signature:** `def post(url, data=None, json=None, **kwargs)`
*   **Description:** This function sends a POST request. It takes the URL for the new :class:`Request` object and optional keyword arguments.
*   **Parameters:**
    *   `url`: The URL for the new :class:`Request` object.
    *   `data`: (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body of the :class:`Request`.
    *   `json`: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    *   `**kwargs`: Optional keyword arguments that can be passed to the function.
*   **Return Value:** A :class:`Response <Response>` object.

#### `put(url, data=None, **kwargs)`

Sends a PUT request.

*   **Signature:** `def put(url, data=None, **kwargs)`
*   **Description:** This function sends a PUT request. It takes the URL for the new :class:`Request` object and optional keyword arguments.
*   **Parameters:**
    *   `url`: The URL for the new :class:`Request` object.
    *   `data`: (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body of the :class:`Request`.
    *   `json`: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    *   `**kwargs`: Optional keyword arguments that can be passed to the function.
*   **Return Value:** A :class:`Response <Response>` object.

#### `patch(url, data=None, **kwargs)`

Sends a PATCH request.

*   **Signature:** `def patch(url, data=None, **kwargs)`
*   **Description:** This function sends a PATCH request. It takes the URL for the new :class:`Request` object and optional keyword arguments.
*   **Parameters:**
    *   `url`: The URL for the new :class:`Request` object.
    *   `data`: (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body of the :class:`Request`.
    *   `json`: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    *   `**kwargs`: Optional keyword arguments that can be passed to the function.
*   **Return Value:** A :class:`Response <Response>` object.

#### `delete(url, **kwargs)`

Sends a DELETE request.

*   **Signature:** `def delete(url, **kwargs)`
*   **Description:** This function sends a DELETE request. It takes the URL for the new :class:`Request` object and optional keyword arguments.
*   **Parameters:**
    *   `url`: The URL for the new :class:`Request` object.
    *   `**kwargs`: Optional keyword arguments that can be passed to the function.
*   **Return Value:** A :class:`Response <Response>` object.

### Usage

```python
>>> import requests
>>> req = requests.request('GET', 'https://httpbin.org/get')
>>> req
<Response [200]>
```

Note: The above usage example is for demonstration purposes only and may not reflect the actual usage of the library.