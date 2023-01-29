This server is queried by the Flutter [app](https://github.com/RenauxLouis/App-Transactions-Record) by sending the data this server will save in a separate Google Sheet

# Query:
```
curl --header "Content-Type: application/json" --request GET '{"code": "75014-01", "machine": "13 kgs"}' "http://<your_url>:8080/add_transaction_row?code=75014-01&machine=13kgs"
```

# Create QR code
In the terminal, use `qr` to convert a string into a QR Code:
```
qr "<your_url>:8080/add_transaction_row?code=75014-01&machine=13kgs" > 75014-01_13kgs.png
```
