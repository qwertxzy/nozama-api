# API Endpoint overview
This document serves as a short overview over the api and its' responses.

 ~~All responses will have the form~~
```json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

~~Following definitions will only show contents of the `data` field.~~
I think most cases can be handled with just http status codes, so that's the approach for now. Every example response is what you're getting.

Furthermore requests may include a `<session_id>` field. This implies that it can only be called after a successful login.

___

## Login / getting a session id

**Definition**

`POST /login`

**Arguments**
- `"username":string` the username used to globally identify a user
- `"password":string` the password of the user in the form of a salted hash with their username

**Response**

- `200 OK` on success
- `400 Bad Request` if provided credentials were incorrect

```json
{
  "session_id": "12345abc"
}

Note this is the only alphanumeric ID

```

## Registering a new account

**Definition**

`POST /register`

**Arguments**
- `"username":string` the desired username
- `"password":string` a hash of a nice and strong password

**Response**

- `200 OK` on success
- `409 Conflict` if the username was taken already

```json
{

}
```

## Purchasing the contents of your current cart

**Definition**

`POST /purchase/<session_id>`

**Arguments**
None

**Response**

- `200 OK` on success
- `401 Unauthorized` if the session_id is not valid

```json
{
  "order_id": 123123123
}
```

## Get item details

**Definition**

`GET /item/<item_id>`

**Response**

- `200 OK` on success
- `404 Not Found` if the item id could not be found

```json
{
  "name": "a product name",
  "description": "a product description",
  "vendor_id": 321
  "pictures": [
    "link/to/pic2",
    "link/to/pic1",
    "etc."
  ],
  "price": 420,
  "category": 111,
  "tags": [
    1,
    2,
    3
  ],
  "details": [
    "whatever",
    "goes",
    "into",
    "here"
  ]
}
```

**Note: another method for batch queries should be created, however I'm still working out the details on that**

## Get tags

**Definition**

`GET /tags`

**Response**

- `200 OK`

```json
{
  "1": "tag1",
  "2": "tag2"
}
```

## Get categories

**Definition**

`GET /categories`

**Response**

- `200 OK`

```json
{
  "1": "cat1",
  "2": "cat2"
}
```

## Get vendor details

**Definition**

`GET /vendor/<vendor_id>`

**Response**

- `200 OK` on success
- `404 Not Found` if the vendor id could not be found

```json
{
  "name": "the vendor name",
  "image": "/path/to/image",
  "description": "a meaningful description",
  "items": [
    123123,
    11,
    231,
  ]
}
```

## Get User details

**Definition**

`GET /profile/<session_id>/`

**Response**

- `200 OK` on success
- `401 Unauthorized` if the session_id is not valid

```json
{
  "name": "username",
  "display_name": "A fancy display name.",
  "wallet": 3.1415,
  "cart": [
    {
      "item_id": 23,
      "amount": 10
    },
    {
      "item_id": 53,
      "amount": 69
    }
  ],
  "order_history": [
    123123,
    321321,
    555
  ]
}
```

## See details of a past order

**Definition**

`GET /order/<session_id>/<order_id>`

**Response**

- `200 OK` on success
- `401 Unauthorized` if the session_id is not valid or if the order_id belongs to a different person
- `404 Not Found` if the order_id could not be found in the database

```json
{
  "ordered_on": "HH:mm DD:MM:YYYY",
  "order_status": "got lost or something idk",
  "order_total": 1000000,
  "items": [
    {
      "item_id": 32,
      "amount": 10
    },
    {
      "item_id": 43,
      "amount": 69
    }
  ]
}
```

## Searching for items by name/tag

**Defitinion**

`GET /search/<search_string>`
The search string searches in product names for now.

**Response**

- `200 OK` in every case
If no items were found, an empty list is provided

```json
{
  "items": [
    1,
    432,
    65
  ]
}
```
