# BookStore Microservice API Documentation
## 1. Overview
This document describes the API for the BookStore Microservice.

## 2. Service List
- Customer Service: http://localhost:8001
- Book Service: http://localhost:8002
- Cart Service: http://localhost:8003
- Staff Service: http://localhost:8004
- Manager Service: http://localhost:8005
- Order Service: http://localhost:8006
- Catalog Service: http://localhost:8007
- Pay Service: http://localhost:8008
- Ship Service: http://localhost:8009
- Comment Rate Service: http://localhost:8010
- Recommender AI Service: http://localhost:8011

## 3. Customer Service API
**Base URL:** `http://localhost:8001`

The customer-service is responsible for customer registration and customer information management.
---
### 3.1. Create Customer
- **Method:** `POST`
- **URL:** `/customers/`
- **Description:** Create a new customer and initialize a cart for them.
- **Request Body:**
```json
{
    "name": "John Doe",
    "email": "[EMAIL_ADDRESS]"
}
```
- **Response:**
```json
{
    "message": "Customer created and cart initialized successfully.",
    "customer": {
        "id": 1,
        "name": "John Doe",
        "email": "[EMAIL_ADDRESS]",
        "created_at": "2022-01-01T00:00:00Z"
    },
    "cart": {
        "id": 1,
        "customer_id": 1,
        "items": [],
        "created_at": "2022-01-01T00:00:00Z"
    }
}
```
## 4. Book Service API
**Base URL:** `http://localhost:8002`

The book-service is responsible for book management.    
---
### 4.1. Create Book
- **Method:** `POST`
- **URL:** `/books/`
- **Description:** Create a new book and initialize a cart for them.
- **Request Body:**
```json
{
    "name": "John Doe",
    "email": "[EMAIL_ADDRESS]"
}
```
- **Response:**
```json
{
    "message": "Customer created and cart initialized successfully.",
    "customer": {
        "id": 1,
        "name": "John Doe",
        "email": "[EMAIL_ADDRESS]",
        "created_at": "2022-01-01T00:00:00Z"
    },
    "cart": {
        "id": 1,
        "customer_id": 1,
        "items": [],
        "created_at": "2022-01-01T00:00:00Z"
    }
}
```
### 4.2. List Books
- **Method:** `GET`
- **URL:** `/books/`
- **Description:** List all books.

#### Success Response

**Status Code:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "price": "19.99",
    "stock": 10,
    "description": "Classic software engineering book"
  }
]
```
## 5. Cart Service API

**Base URL:** `http://localhost:8003`

The cart-service manages shopping carts and cart items.

---

### 5.1 Add Item to Cart

- **Method:** `POST`
- **URL:** `/cart-items/`
- **Description:** Add a book to the customer's cart. The service validates the book by calling `book-service`.

#### Request Body

```json
{
  "customer_id": 1,
  "book_id": 1,
  "quantity": 2
}
```

#### Success Response

**Status Code:** `201 Created`

```json
{
  "id": 1,
  "cart": 1,
  "book_id": 1,
  "quantity": 2
}
```

#### Error Response

**Status Code:** `404 Not Found`

```json
{
  "error": "Book not found"
}
```

---

### 5.2 View Cart

- **Method:** `GET`
- **URL:** `/carts/{customer_id}/`
- **Description:** View all items in a customer cart.

#### Example URL

```text
/carts/1/
```

#### Success Response

**Status Code:** `200 OK`

```json
[
  {
    "id": 1,
    "cart": 1,
    "book_id": 1,
    "quantity": 2
  }
]
```



## 6. Staff Service API
**Base URL:** `http://localhost:8004`

The staff-service is responsible for staff management.

---

### 6.1. Create Staff
- **Method:** `POST`
- **URL:** `/staffs/`
- **Description:** Create a new staff and initialize a cart for them.
- **Request Body:**
```json
{
    "name": "John Doe",
    "email": "[EMAIL_ADDRESS]"
}
```
- **Response:**
```json
{
    "message": "Customer created and cart initialized successfully.",
    "customer": {
        "id": 1,
        "name": "John Doe",
        "email": "[EMAIL_ADDRESS]",
        "created_at": "2022-01-01T00:00:00Z"
    },
    "cart": {
        "id": 1,
        "customer_id": 1,
        "items": [],
        "created_at": "2022-01-01T00:00:00Z"
    }
}
```
### 6.2. List Staffs
- **Method:** `GET`
- **URL:** `/staffs/`
- **Description:** List all staffs.

#### Success Response

**Status Code:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "price": "19.99",
    "stock": 10,
    "description": "Classic software engineering book"
  }
]
```

## 7. Manager Service API
**Base URL:** `http://localhost:8005`

The manager-service is responsible for manager management.

---

### 7.1. Create Manager
- **Method:** `POST`
- **URL:** `/managers/`
- **Description:** Create a new manager and initialize a cart for them.
- **Request Body:**
```json
{
    "name": "John Doe",
    "email": "[EMAIL_ADDRESS]"
}
```
- **Response:**
```json
{
    "message": "Customer created and cart initialized successfully.",
    "customer": {
        "id": 1,
        "name": "John Doe",
        "email": "[EMAIL_ADDRESS]",
        "created_at": "2022-01-01T00:00:00Z"
    },
    "cart": {
        "id": 1,
        "customer_id": 1,
        "items": [],
        "created_at": "2022-01-01T00:00:00Z"
    }
}
```
### 7.2. List Managers
- **Method:** `GET`
- **URL:** `/managers/`
- **Description:** List all managers.

#### Success Response

**Status Code:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "price": "19.99",
    "stock": 10,
    "description": "Classic software engineering book"
  }
]
```

## 8. Order Service API
**Base URL:** `http://localhost:8006`

The order-service is responsible for order management.

---

### 8.1. Create Order
- **Method:** `POST`
- **URL:** `/orders/`
- **Description:** Create a new order and initialize a cart for them.
- **Request Body:**
```json
{
    "name": "John Doe",
    "email": "[EMAIL_ADDRESS]"
}
```
- **Response:**
```json
{
    "message": "Customer created and cart initialized successfully.",
    "customer": {
        "id": 1,
        "name": "John Doe",
        "email": "[EMAIL_ADDRESS]",
        "created_at": "2022-01-01T00:00:00Z"
    },
    "cart": {
        "id": 1,
        "customer_id": 1,
        "items": [],
        "created_at": "2022-01-01T00:00:00Z"
    }
}
```
### 8.2. List Orders
- **Method:** `GET`
- **URL:** `/orders/`
- **Description:** List all orders.

#### Success Response

**Status Code:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "price": "19.99",
    "stock": 10,
    "description": "Classic software engineering book"
  }
]
```

## 9. Catalog Service API
**Base URL:** `http://localhost:8007`

The catalog-service is responsible for catalog management.

---

### 9.1. Create Catalog
- **Method:** `POST`
- **URL:** `/catalogs/`
- **Description:** Create a new catalog and initialize a cart for them.
- **Request Body:**
```json
{
    "name": "John Doe",
    "email": "[EMAIL_ADDRESS]"
}
```
- **Response:**
```json
{
    "message": "Customer created and cart initialized successfully.",
    "customer": {
        "id": 1,
        "name": "John Doe",
        "email": "[EMAIL_ADDRESS]",
        "created_at": "2022-01-01T00:00:00Z"
    },
    "cart": {
        "id": 1,
        "customer_id": 1,
        "items": [],
        "created_at": "2022-01-01T00:00:00Z"
    }
}
```
### 9.2. List Catalogs
- **Method:** `GET`
- **URL:** `/catalogs/`
- **Description:** List all catalogs.

#### Success Response

**Status Code:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "price": "19.99",
    "stock": 10,
    "description": "Classic software engineering book"
  }
]
```

## 10. Pay Service API
**Base URL:** `http://localhost:8008`

The pay-service is responsible for pay management.

---

### 10.1. Create Pay
- **Method:** `POST`
- **URL:** `/pays/`
- **Description:** Create a new pay and initialize a cart for them.
- **Request Body:**
```json
{
    "name": "John Doe",
    "email": "[EMAIL_ADDRESS]"
}
```
- **Response:**
```json
{
    "message": "Customer created and cart initialized successfully.",
    "customer": {
        "id": 1,
        "name": "John Doe",
        "email": "[EMAIL_ADDRESS]",
        "created_at": "2022-01-01T00:00:00Z"
    },
    "cart": {
        "id": 1,
        "customer_id": 1,
        "items": [],
        "created_at": "2022-01-01T00:00:00Z"
    }
}
```
### 10.2. List Pays
- **Method:** `GET`
- **URL:** `/pays/`
- **Description:** List all pays.

#### Success Response

**Status Code:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "price": "19.99",
    "stock": 10,
    "description": "Classic software engineering book"
  }
]
```

## 11. Ship Service API
**Base URL:** `http://localhost:8009`

The ship-service is responsible for ship management.

---

### 11.1. Create Ship
- **Method:** `POST`
- **URL:** `/ships/`
- **Description:** Create a new ship and initialize a cart for them.
- **Request Body:**
```json
{
    "name": "John Doe",
    "email": "[EMAIL_ADDRESS]"
}
```
- **Response:**
```json
{
    "message": "Customer created and cart initialized successfully.",
    "customer": {
        "id": 1,
        "name": "John Doe",
        "email": "[EMAIL_ADDRESS]",
        "created_at": "2022-01-01T00:00:00Z"
    },
    "cart": {
        "id": 1,
        "customer_id": 1,
        "items": [],
        "created_at": "2022-01-01T00:00:00Z"
    }
}
```
### 11.2. List Ships
- **Method:** `GET`
- **URL:** `/ships/`
- **Description:** List all ships.

#### Success Response

**Status Code:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "price": "19.99",
    "stock": 10,
    "description": "Classic software engineering book"
  }
]
```

## 12. Comment-Rate Service API
**Base URL:** `http://localhost:8010`

The comment-rate-service is responsible for comment-rate management.

---

### 12.1. Create Comment-Rate
- **Method:** `POST`
- **URL:** `/comment-rates/`
- **Description:** Create a new comment-rate and initialize a cart for them.
- **Request Body:**
```json
{
    "name": "John Doe",
    "email": "[EMAIL_ADDRESS]"
}
```
- **Response:**
```json
{
    "message": "Customer created and cart initialized successfully.",
    "customer": {
        "id": 1,
        "name": "John Doe",
        "email": "[EMAIL_ADDRESS]",
        "created_at": "2022-01-01T00:00:00Z"
    },
    "cart": {
        "id": 1,
        "customer_id": 1,
        "items": [],
        "created_at": "2022-01-01T00:00:00Z"
    }
}
```
### 12.2. List Comment-Rates
- **Method:** `GET`
- **URL:** `/comment-rates/`
- **Description:** List all comment-rates.

#### Success Response

**Status Code:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "price": "19.99",
    "stock": 10,
    "description": "Classic software engineering book"
  }
]
```

## 13. Recommender AI Service API
**Base URL:** `http://localhost:8011`

The recommender-ai-service is responsible for recommender-ai management.

---

### 13.1. Create Recommender AI
- **Method:** `POST`
- **URL:** `/recommender-ais/`
- **Description:** Create a new recommender-ai and initialize a cart for them.
- **Request Body:**
```json
{
    "name": "John Doe",
    "email": "[EMAIL_ADDRESS]"
}
```
- **Response:**
```json
{
    "message": "Customer created and cart initialized successfully.",
    "customer": {
        "id": 1,
        "name": "John Doe",
        "email": "[EMAIL_ADDRESS]",
        "created_at": "2022-01-01T00:00:00Z"
    },
    "cart": {
        "id": 1,
        "customer_id": 1,
        "items": [],
        "created_at": "2022-01-01T00:00:00Z"
    }
}
```
### 13.2. List Recommender AIs
- **Method:** `GET`
- **URL:** `/recommender-ais/`
- **Description:** List all recommender-ais.

#### Success Response

**Status Code:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "price": "19.99",
    "stock": 10,
    "description": "Classic software engineering book"
  }
]
```

