# Macaque
Flask style library for microservices with [MQ Light](https://developer.ibm.com/messaging/mq-light/)

```python
import macaque
```
Importing the macaque library into your application code

```python
srv = macaque.Server()
```
Creating an instance of the macaque server component

```python
@srv.service("news/technology")
def news_tech_handler(request):
	print request
	return {"headline": "MQ Light rocks!"}
```
Creating a service endpoint handler

```python
cl = macaque.Client()
```
Creating an instance of the macaque client component

```python
def response_handler(response):
    print response['headline']

app.call("news/technology", "MQ Light?", response_handler)
```
Calling a service endpoint and handling the returned value

This project is licensed under the Eclipse Public License, details can be found in the file `LICENSE`