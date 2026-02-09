# Requests API - Main Interface (Official Documentation)

> Source: https://requests.readthedocs.io/en/latest/api/

All of Requests' functionality can be accessed by these 7 methods. They all return an instance of the `Response` object.

## requests.request(method, url, **kwargs)

Constructs and sends a `Request`.

### Parameters

- **method** – method for the new Request object: GET, OPTIONS, HEAD, POST, PUT, PATCH, or DELETE.
- **url** – URL for the new Request object.
- **params** – (optional) Dictionary, list of tuples or bytes to send in the query string for the Request.
- **data** – (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body of the Request.
- **json** – (optional) A JSON serializable Python object to send in the body of the Request.
- **headers** – (optional) Dictionary of HTTP Headers to send with the Request.
- **cookies** – (optional) Dict or CookieJar object to send with the Request.
- **files** – (optional) Dictionary of 'name': file-like-objects for multipart encoding upload.
- **auth** – (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
- **timeout** (float or tuple) – (optional) How many seconds to wait for the server to send data before giving up.
- **allow_redirects** (bool) – (optional) Boolean. Enable/disable redirection. Defaults to True.
- **proxies** – (optional) Dictionary mapping protocol to the URL of the proxy.
- **verify** – (optional) Either a boolean for TLS certificate verification, or a path to a CA bundle.
- **stream** – (optional) if False, the response content will be immediately downloaded.
- **cert** – (optional) path to ssl client cert file (.pem) or ('cert', 'key') tuple.

### Returns

`requests.Response` object

### Usage

```python
>>> import requests
>>> req = requests.request('GET', 'https://httpbin.org/get')
>>> req
<Response [200]>
```

---

## requests.head(url, **kwargs)

Sends a HEAD request.

### Parameters

- **url** – URL for the new Request object.
- ****kwargs** – Optional arguments that `request` takes. If `allow_redirects` is not provided, it will be set to False.

### Returns

`requests.Response` object

---

## requests.get(url, params=None, **kwargs)

Sends a GET request.

### Parameters

- **url** – URL for the new Request object.
- **params** – (optional) Dictionary, list of tuples or bytes to send in the query string.
- ****kwargs** – Optional arguments that `request` takes.

### Returns

`requests.Response` object

---

## requests.post(url, data=None, json=None, **kwargs)

Sends a POST request.

### Parameters

- **url** – URL for the new Request object.
- **data** – (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body.
- **json** – (optional) A JSON serializable Python object to send in the body.
- ****kwargs** – Optional arguments that `request` takes.

### Returns

`requests.Response` object

---

## requests.put(url, data=None, **kwargs)

Sends a PUT request.

### Parameters

- **url** – URL for the new Request object.
- **data** – (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body.
- **json** – (optional) A JSON serializable Python object to send in the body.
- ****kwargs** – Optional arguments that `request` takes.

### Returns

`requests.Response` object

---

## requests.patch(url, data=None, **kwargs)

Sends a PATCH request.

### Parameters

- **url** – URL for the new Request object.
- **data** – (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body.
- **json** – (optional) A JSON serializable Python object to send in the body.
- ****kwargs** – Optional arguments that `request` takes.

### Returns

`requests.Response` object

---

## requests.delete(url, **kwargs)

Sends a DELETE request.

### Parameters

- **url** – URL for the new Request object.
- ****kwargs** – Optional arguments that `request` takes.

### Returns

`requests.Response` object
