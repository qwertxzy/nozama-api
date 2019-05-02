# API Endpoint overview
This document serves as a short overview over the api and its' responses.

All responses will have the form
```json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

Following definitions will only show contents of the `data` field.
Furthermore requests may include a `<session_id>` field. This implies that it can only be called after a successful login.

___

##Login / getting a session id

**Definition**

`POST /login`

**Arguments**
-`"username":string` the username used to globally identify a user
-`"password":string` the password of the user in the form of a salted hash with their username

**Response**

- `200 OK` on success
- `400 Bad Request` if provided credentials were incorrect

```json
{
  "session_id": "12345abc"
}

```

##Get item details

**Definition**

`GET /item/<item_id>`

**Response**

- `200 OK` on success
- `404 Not Found` if the item id could not be found

```json
{
  "message": "successful",
  "item_id": "the item id",
  "data": {
    "name": "a product name",
    "description": "a product description",
    "vendor": "the vendor’s id",
    "pictures": [
      "link/to/pic2",
      "link/to/pic1",
      "etc."
    ],
    "price": 420,
    "categories": [
      "category1",
      "category2",
      "etc."
    ],
    "tags": [
      "tag1",
      "tag2",
      "etc."
    ],
    "details": [
      "whatever",
      "goes",
      "into",
      "here"
    ]
  }
}
```

**Note: another method for batch queries should be created, however I'm still working out the details on that**

##Get vendor details

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
    "item_id1",
    "item_id2",
    "etc.",
  ]
}
```

##Get User details

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
      "item_id": "xyz",
      "amount": 10
    },
    {
      "item_id": "nice",
      "amount": 69
    }
  ],
  "order_history": [
    "order_id1",
    "order_id2",
    "etc."
  ]
}
```

##See details of a past order

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
      "item_id": "xyz",
      "amount": 10
    },
    {
      "item_id": "nice",
      "amount": 69
    }
  ]
}
```

##Searching for items by name/tag

**Defitinion**

`GET /search/<search_string>`
The search string searches in product names for now.

**Response**

-`200 OK` in every case
If no items were found, an empty list is provided

```json
{
  "items": [
    "item_id1",
    "item_id2",
    "etc."
  ]
}
```
