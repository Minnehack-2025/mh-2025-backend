# API Endpoints Documentation

## Users

### Get All Users
- **URL:** `/users`
- **Method:** `GET`
- **Description:** Retrieve a list of all users.
- **Response:**
  - `200 OK`: Returns a list of user representations.
  - `500 Internal Server Error`: Returns an error message.

### Create User
- **URL:** `/users`
- **Method:** `POST`
- **Description:** Create a new user.
- **Request Body:**
  - `username` (string): The username of the user.
  - `email` (string): The email of the user.
  - `password` (string): The password of the user.
  - `interests` (JSON): The interests of the user (optional).
  - `availability` (JSON): The availability of the user (optional).
  - `image` (file): The profile image of the user (optional).
- **Response:**
  - `201 Created`: Returns the created user representation.
  - `500 Internal Server Error`: Returns an error message.

### Update User
- **URL:** `/users/<int:user_id>`
- **Method:** `PUT`
- **Description:** Update an existing user.
- **Request Body:**
  - `username` (string): The username of the user (optional).
  - `email` (string): The email of the user (optional).
  - `password` (string): The password of the user (optional).
  - `interests` (JSON): The interests of the user (optional).
  - `availability` (JSON): The availability of the user (optional).
  - `image` (file): The profile image of the user (optional).
- **Response:**
  - `200 OK`: Returns the updated user representation.
  - `500 Internal Server Error`: Returns an error message.

### Delete User
- **URL:** `/users/<int:user_id>`
- **Method:** `DELETE`
- **Description:** Delete an existing user.
- **Response:**
  - `204 No Content`: Indicates successful deletion.
  - `500 Internal Server Error`: Returns an error message.

### Login User
- **URL:** `/users/login`
- **Method:** `POST`
- **Description:** Login a user.
- **Request Body:**
  - `email` (string): The email of the user.
  - `password` (string): The password of the user.
- **Response:**
  - `200 OK`: Returns a success message.
  - `401 Unauthorized`: Returns an error message for invalid credentials.
  - `500 Internal Server Error`: Returns an error message.

## Events

### Get All Events
- **URL:** `/events`
- **Method:** `GET`
- **Description:** Retrieve a list of events.
- **Query Parameters:**
  - `number` (int): The number of events to retrieve (default is 10).
- **Response:**
  - `200 OK`: Returns a list of event representations.
  - `500 Internal Server Error`: Returns an error message.

### Create Event
- **URL:** `/events`
- **Method:** `POST`
- **Description:** Create a new event.
- **Request Body:**
  - `name` (string): The name of the event.
  - `description` (string): The description of the event (optional).
  - `location` (string): The location of the event.
  - `time` (string): The time of the event in ISO format.
  - `user_id` (int): The ID of the user creating the event.
  - `image` (file): The image of the event (optional).
- **Response:**
  - `201 Created`: Returns the created event representation.
  - `500 Internal Server Error`: Returns an error message.

### Get Event by ID
- **URL:** `/events/<int:event_id>`
- **Method:** `GET`
- **Description:** Retrieve an event by its ID.
- **Response:**
  - `200 OK`: Returns the event representation.
  - `500 Internal Server Error`: Returns an error message.

### Update Event
- **URL:** `/events/<int:event_id>`
- **Method:** `PUT`
- **Description:** Update an existing event.
- **Request Body:**
  - `name` (string): The name of the event (optional).
  - `description` (string): The description of the event (optional).
  - `location` (string): The location of the event (optional).
  - `time` (string): The time of the event in ISO format (optional).
  - `image` (file): The image of the event (optional).
- **Response:**
  - `200 OK`: Returns the updated event representation.
  - `500 Internal Server Error`: Returns an error message.

### Delete Event
- **URL:** `/events/<int:event_id>`
- **Method:** `DELETE`
- **Description:** Delete an existing event.
- **Response:**
  - `204 No Content`: Indicates successful deletion.
  - `500 Internal Server Error`: Returns an error message.

## Images

### Upload Image
- **URL:** `/upload`
- **Method:** `POST`
- **Description:** Upload a new image.
- **Request Body:**
  - `file` (file): The image file to upload.
- **Response:**
  - `201 Created`: Returns a success message and the image ID.
  - `400 Bad Request`: Returns an error message for invalid file.
  - `500 Internal Server Error`: Returns an error message.

### Serve Image
- **URL:** `/uploads/<int:image_id>`
- **Method:** `GET`
- **Description:** Retrieve an image by its ID.
- **Response:**
  - `200 OK`: Returns the image file.
  - `404 Not Found`: Returns an error message if the image is not found.

## Test Database Connection

### Test Database Connection
- **URL:** `/test-db`
- **Method:** `GET`
- **Description:** Test the database connection.
- **Response:**
  - `200 OK`: Returns a success message if the connection is successful.
  - `500 Internal Server Error`: Returns an error message if the connection fails.