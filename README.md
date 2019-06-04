# API Endpoint overview
This document serves as a short overview over the api and its' responses.

Furthermore requests may include a `<session_id>` field. This implies that it can only be called after a successful login.

___

## Account

### Login / getting a session id

**Definition**

`POST /login`

**Arguments**
- `"email":string` the email address used to globally identify a user
- `"password":string` the user's password

**Response**

- `200 OK` on success
- `401 Unauthorized` if provided credentials were incorrect

```json
{
  "session_id": "595743e4fc699393"
}
```
Note this is the only alphanumeric ID at 16 characters length

### Registering a new account

**Definition**

`POST /register`

**Arguments**
- `"email":string` the user's e-mail address (**has to be globally unique**)
- `"username":string` the desired username used for displaying
- `"password":string` a hash of a nice and strong password

**Response**

- `200 OK` on success
- `409 Conflict` if the email is already being used

### Changing your password

**Definition**

`POST /change_password/<session_id>`

**Arguments**
- `"password":string` the new password to be used

**Response**

- `200 OK` on success
- `400 Bad Request` if the session_id is too long
- `401 Unauthorized` if the session id is invalid
- `409 Conflict` if the password is identical to the existing one

### Get user details

**Definition**

`GET /profile/<session_id>/`

**Response**

- `200 OK` on success
- `401 Unauthorized` if the session_id could not be found
- `400 Bad Request` if the session_id is too long

```json
{
  "name": "a fancy name",
  "belongs_to_vendor": 1,
  "city": "wewlad",
  "zip": "123456",
  "street": "yeet yoot",
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

### Change user details

**Definition**

`POST /change_profile/user/<session_id>`

```json
{
  "name": "a new name?",
  "leave_vendor": true
}
```

Note: even if a vendor ends up with 0 members this way, it will still continue to exist, but all of this vendor's items will be hidden for future purchases.

**Response**

- `200 OK` on success
- `400 Bad Request` if the session_id is too long
- `401 Unauthorized` if the session_id is invalid

## Change your delivery address

**Definition**

`POST /change_address/<session_id>`

```json
{
  "city": "Ye olde town",
  "zip": "666666",
  "street": "You know where"
}
```

**Response**

- `200 OK` on success
- `400 Bad Request` if the session_id is too long
- `401 Unauthorized` if the session_id is invalid

### Add funds to your wallet

**Definition**

`POST /add_funds/<session_id>/<amount>`

**Response**

- `200 OK` on success
- `400 Bad Request` if the session_id is too long
- `401 Unauthorized` if the session_id is invalid

### Open up a new vendor page

**Definition**

`POST /add_vendor/<session_id>`

```json
{
  "name": "a cool vendor name",
  "description": "why you're so cool"
}
```

**Response**

- `200 OK` on success
- `400 Bad Request` if the session_id is too long
- `401 Unauthorized` if the session_id is invalid

### Adding an image to your vendor page

**Definition**

`POST /add_vendor_image/<session_id>`

`enctype=multipart/form-data`

**Arguments**

- `"image":file` the image to be added

**Response**

- `200 OK` on success
- `400 Bad Request` if the session_id was too long
- `401 Unauthorized` if the session id was not valid or if the user does not belong to any vendor

If the file was already present it will be overwritten.

### Add a vendor page member

**Definition**

`POST /add_vendor_member/<session_id>/<email>`

**Response**

- `200 OK` on success
- `400 Bad Request` if the session_id is too long
- `401 Unauthorized` if the session_id is invalid
- `404 Not Found` if the user e-mail could not be found

### Change vendor details

**Definition**

`POST /change_profile/vendor/<session_id>`

```json
{
  "name": "your new name?",
  "description": "a fresh breeze.."
}
```

**Response**

- `200 OK` on success
- `400 Bad Request` if the session_id is too long
- `401 Unauthorized` if the session_id is invalid

## Item

### Get item details

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
    "beautiful",
    "another tag"
  ],
  "details": {
   "property 1": "value1",
   "property 2": "value2"
 }
}
```

**Note: another method for batch queries should be created, however I'm still working out the details on that**

### Add a product to your vendor page

**Definition**

`POST /add_item/<session_id>`

```json
{
  "name": "a product name",
  "description": "a product description",
  "manufacturer": 1,
  "price": 420,
  "category": 111,
  "tags": [
    "one",
    "two",
    "three"
  ],
  "details": {
    "property 1": "value1",
    "property 2": "value2"
  }
}
```

**Response**

- `200 OK` on success
- `400 Bad Request` if the request was not valid or if the session_id was too long
- `401 Unauthorized` if the session_id was invalid or if the user is not part of any vendor

```json
{
  "item_id": 123
}
```

### Adding an image to an item

**Definition**

`POST /add_item_image/<session_id>/<item_id>`

**Arguments**

- `"image":file` the image to be added

**Response**

- `200 OK` on success
- `400 Bad Request` if the file was invalid or if the session_id was too long
- `401 Unauthorized` if the session id was not valid

### Adding a tag to an item

**Definition**

`POST /add_item_tag/<item_id>/<tag_name>`

**Response**

- `200 OK` on success
- `404 Not Found` if the Item or Tag ID was not found

### Editing existing item information

**Definition**

`POST /change_item/info/<session_id>/<item_id>`

```json
{
  "name": "a new product name",
  "description": "a new product description",
  "manufacturer": 2,
  "price": 1000,
  "category": 4,
  "tags": [
    "four",
    "five",
    "six"
  ]
}
```

**Response**

- `200 OK` on success
- `404 Not Found` if the item_id could not be found
- `401 Unauthorized` if the session_id was invalid or if the user does not belong to that item's vendor
- `400 Bad Request` if the session_id provided was too long

### Editing existing item details

**Definition**

`POST /change_item/details/<sesison_id>/<item_id>`

```json
{
  "property 1": "new value1",
  "property 2": "new value2"
}
```

**Response**

- `200 OK` on success
- `404 Not Found` if the item_id could not be found
- `401 Unauthorized` if the session_id was invalid or if the user does not belong to that item's vendor
- `400 Bad Request` if the session_id provided was too long

### Delete an item's image

**Definition**

`POST /remove_item_image/<session_id>/<item_id>/<image_file_name>`

**Response**

- `200 OK` on success
- `404 Not Found` if the item_id or image file could not be found
- `401 Unauthorized` if the session_id was invalid or if the user does not belong to that item's vendor
- `400 Bad Request` if the session_id provided was too long

### Deleting an item from your vendor page

**Definition**

`POST /delete_item/<session_id>/<item_id>`

**Response**

- `200 OK` on success
- `401 Unauthorized` if the session_id is invalid
- `404 Not Found` if the item_id could not be found or if the item does not belong to the vendor

Note that this does not actually delete the item from the database, but just hide it from being selected for new purchases.

### Putting an item into your cart

**Definition**

`POST /grab_item/<session_id>/<item_id>/<amount>`

**Response**

- `200 OK` on success
- `404 Not Found` if the item could not be found
- `401 Unauthorized` if the session id could not be found
- `400 Bad Request` if the session_id is too long
- `403 Forbidden` if the amount is < 0

### Removing an item from your cart

**Definition**

`POST /remove_item/<session_id>/<item_id>`

**Response**

- `200 OK` on success
- `404 Not Found` if the item could not be found
- `401 Unauthorized` if the session id could not be found
- `400 Bad Request` if the session_id is too long

### Get tags

**Definition**

`GET /tags`

**Response**

- `200 OK`

```json
[
  "Tag one",
  "Tag two",
  "Tag three"
]
```

### Get categories

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

### Get manufacturers

**Definition**

`GET /manufacturers`

**Response**

- `200 OK`

```json
[
  {
    "manufacturer_name": "wew",
    "manufacturer_description": "wow",
    "manufacturer_id": 1
  },
  {
    "manufacturer_name": "lad",
    "manufacturer_description": "i don't even know anymore",
    "manufacturer_id": 2
  }
]
```

### Adding a manufacturer

**Definition**

`POST /add_manufacturer/<manufacturer_name>`

**Response**

- `200 OK`

```json
{
  "manufacturer_name": "lad",
  "manufacturer_id": 2
}
```

### Get vendor details

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
    231
  ]
}
```

### Searching for items by name/tag

**Defitinion**

`GET /search/<search_string>`
The search string searches in product names for now.

**Response**

- `200 OK` in every case
If no items were found, an empty list is provided

```json
[
  1,
  432,
  65
]

```

### Get n  random items

**Definition**

`GET /random/<amount>`

**Response**

- `200 OK` on success
- `400 Bad Request` if the amount is < 1

```json
[
  1,
  2,
  3,
  4,
  69
]
```

## Order

### Purchasing the contents of your current cart

**Definition**

`POST /purchase/<session_id>`


**Response**

- `200 OK` on success
- `400 Bad Request` if the cart was empty
- `401 Unauthorized` if the session_id is invalid

```json
{
  "order_id": 123123123
}
```

### See details of a past order

**Definition**

`GET /order/<session_id>/<order_id>`

**Response**

- `200 OK` on success
- `401 Unauthorized` if the session_id is not valid or if the order_id belongs to a different person
- `404 Not Found` if the order_id could not be found in the database
- `400 Bad Request` if the session_id was longer than 16 characters

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
