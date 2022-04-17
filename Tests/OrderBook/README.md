## How to use OrderBook
### Request object
#### Create ASK request
```python
from Tests.OrderBook.Requests import AskRequest

ask_request = AskRequest(price=1, volume=1)
```
#### Create BID request
```python
from Tests.OrderBook.Requests import BidRequest

ask_request = BidRequest(price=1, volume=1)
```
### OrderBook object
#### Add request
```python
from Tests.OrderBook.OrderBook import OrderBook
from Tests.OrderBook.Requests import Request

request = Request(price=1, volume=1)
order_book = OrderBook()
order_book.add_request(request)
```
#### Add multiple requests
```python
from Tests.OrderBook.OrderBook import OrderBook
from Tests.OrderBook.Requests import Request

requests = [Request(price=1, volume=1) for _ in range(10)]
order_book = OrderBook()
order_book.add_requests(requests)
```
#### Delete request
```python
from Tests.OrderBook.OrderBook import OrderBook
from Tests.OrderBook.Requests import Request

request = Request(price=1, volume=1)
order_book = OrderBook()
order_book.add_request(request)
order_book.delete_request(request.id)
```
#### Change request info
```python
from Tests.OrderBook.OrderBook import OrderBook
from Tests.OrderBook.Requests import Request

request = Request(price=1, volume=1)
order_book = OrderBook()
order_book.add_request(request)
order_book.change_request_info(request.id, price=123, volume=123)
```
#### Get request info
```python
from Tests.OrderBook.OrderBook import OrderBook
from Tests.OrderBook.Requests import Request

request = Request(price=1, volume=1)
order_book = OrderBook()
order_book.add_request(request)
request_info = order_book.get_request_info(request.id)
```
#### Get snapshot
```python
from Tests.OrderBook.OrderBook import OrderBook

order_book = OrderBook()
snapshot = order_book.get_snapshot()
```