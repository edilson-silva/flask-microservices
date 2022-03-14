# Flask Microservices
Flask store application based on microservices architecture

<br />

## List of microservices

[User](user/README.md)

[Book](book/README.md)

[Order](order/README.md)

<br />

## Notes

To generate the `SECRET_KEY` environment variables of the microservices, the `secrets` module of python was used, but it can contain any value.\
Note: For security reasons it is preferable that this value is a hash.


Example code:
```python
import secrets

secrets.token_urlsafe(16)
```
