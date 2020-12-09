# lavey-livrey-qrcode
Lavey Livrey QR Code server

# Query:
```
curl --header "Content-Type: application/json" --request GET '{"code": "75014-01", "machine": "13 kgs"}' "http://<your_url>:8080/add_transaction_row?code=75014-01&machine=13kgs"
```

# Create QR code
In the terminal, use `qr` to convert a string into a QR Code:
```
qr "<your_url>:8080/add_transaction_row?code=75014-01&machine=13kgs" > 75014-01_13kgs.png
```
