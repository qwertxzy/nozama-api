# API Endpoint overview
This document serves as a short overview over the api and its' responses.

Furthermore requests may include a `<session_id>` field. This implies that it can only be called after a successful login.

___

## Login / getting a session id

**Definition**

`POST /login`

**Arguments**
- `"email":string` the email address used to globally identify a user
- `"password":string` the user's password

**Response**

- `200 OK` on success
- `400 Bad Request` if provided credentials were incorrect

```json
{
  "session_id": "12345abc"
}
```
Note this is the only alphanumeric ID

## Registering a new account

**Definition**

`POST /register`

**Arguments**
- `"email":string` the user's e-mail address (**has to be globally unique**)
- `"username":string` the desired username used for displaying
- `"password":string` a hash of a nice and strong password

**Response**

- `200 OK` on success
- `409 Conflict` if the email is already being used

## Changing your password

**Definition**

`POST /change_password/<session_id>`

**Arguments**
- `"email":string` the user's email address
- `"password":string` the new password to be used

**Response**

- `200 OK` on success
- `401 Unauthorized` if the session id is invalid

## Purchasing the contents of your current cart

**Definition**

`POST /purchase/<session_id>`


**Response**

- `200 OK` on success
- `401 Unauthorized` if the session_id is invalid

```json
{
  "order_id": 123123123
}
```

## Add a product to your vendor page

**Definition**

`POST /add_item/<session_id>`


**Request Body**
```json
{
  "name": "a product name",
  "description": "a product description",
  "vendor": 2,
  "manufacturer": 1,
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

**Response**

- `200 OK` on success
- `400 Bad Request` if the request was not valid

```json
{
  "item_id": 123
}
```

## Deleting an item from your vendor page

**Definition**

`POST /remove_item/<session_id>/<item_id>`

**Response**

- `200 OK` on success
- `401 Unauthorized` if the session_id is invalid or if the item does not belong to the vendor
- `404 Not Found` if the item_id could not be found

## Adding an image to an item

**Definition**

`POST /add_item_image/<session_id/<image_id>`

`enctype=multipart/form-data`

**Arguments**

- `"image":file` the image to be added

**Response**

- `200 OK` on success
- `400 Bad Request` if the file was invalid

## Adding a tag

**Definition**

`POST /add_tag/<tag_name>`

**Response**

- `200 OK` on success
- `401 Bad Request` if the tag name is already being used

```json
{
  "tag_id": 9
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
  "vendor": 2,
  "manufacturer": 1,
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
[
  {
    "tag_name": "abc",
    "tag_id": 1
  },
  {
    "tag_name": "def",
    "tag_id": 2
  }
]
```

## Get categories

**Definition**

`GET /categories`

**Response**

- `200 OK`

```json
[
  {
    "category_name": "abc",
    "category_id": 1
  },
  {
    "category_name": "def",
    "category_id": 2
  }
]
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
