### Description for lñine protocol to write data in InfluxDB3

- Table: A string that identifies the table to store data in
- tag set: Comma-delimited list of key value pairs, each representing a tag
- field set: Key-value pairs between the first and second unscaped whitespaces
- timestamp: Integer value after the second unescaped whitespace

> myTable,tag1=val1,tag2=val2 field1="v1",field2=1i 0000000000000000000

example:
```
Table: home
- tags
  - room: Living Room or Kitchen
- fields
    temp: temperature in °C (float)
    hum: percent humidity (float)
    co: carbon monoxide in parts per million (integer)
timestamp: Unix timestamp in second precision
```