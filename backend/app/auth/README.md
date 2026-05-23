```shell
openssl genrsa -out jwt-private.pem 2048
```

```shell
openssl rsa -in jwt-private.pem -outform PEM -pubour -out jwt-public.pem
```
