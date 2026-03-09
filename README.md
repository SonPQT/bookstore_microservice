# BookStore Microservice - Stage 3

Project này bám theo appendix của đề: mỗi service là một Django project riêng, giao tiếp qua REST, chạy bằng Docker Compose. Bản Stage 3 mở rộng Stage 2 để tiến gần đầy đủ Assignment 05.

## Danh sách service

### Core đã có từ Stage 1 + Stage 2
- customer-service
- book-service
- cart-service
- staff-service
- manager-service
- order-service
- api-gateway

### Bổ sung ở Stage 3
- catalog-service
- pay-service
- ship-service
- comment-rate-service
- recommender-ai-service

## Kiến trúc hiện tại

```text
API Gateway
  |
  +-- customer-service ---> cart-service
  +-- staff-service ------> book-service
  +-- catalog-service ----> book-service, comment-rate-service
  +-- order-service ------> cart-service, book-service, pay-service, ship-service
  +-- recommender-ai -----> book-service, comment-rate-service
  +-- manager-service ----> all service health/count summary
```

## Chạy nhanh

```bash
docker compose up --build
```

## Port

- gateway: http://localhost:8000
- customer-service: http://localhost:8001
- book-service: http://localhost:8002
- cart-service: http://localhost:8003
- staff-service: http://localhost:8004
- manager-service: http://localhost:8005
- order-service: http://localhost:8006
- catalog-service: http://localhost:8007
- pay-service: http://localhost:8008
- ship-service: http://localhost:8009
- comment-rate-service: http://localhost:8010
- recommender-ai-service: http://localhost:8011

## Flow demo ngắn nhất

### 1. Tạo staff
```bash
curl -X POST http://localhost:8004/staff/   -H "Content-Type: application/json"   -d '{"name":"Staff A","email":"staffa@example.com"}'
```

### 2. Tạo book
```bash
curl -X POST http://localhost:8004/staff/books/   -H "Content-Type: application/json"   -d '{"title":"Clean Code","author":"Robert C. Martin","price":"19.99","stock":10,"description":"Classic book"}'
```

### 3. Tạo customer
```bash
curl -X POST http://localhost:8001/customers/   -H "Content-Type: application/json"   -d '{"name":"Alice","email":"alice@example.com"}'
```

### 4. Thêm sách vào cart
```bash
curl -X POST http://localhost:8003/cart-items/   -H "Content-Type: application/json"   -d '{"customer_id":1,"book_id":1,"quantity":2}'
```

### 5. Tạo order, chọn payment và shipping
```bash
curl -X POST http://localhost:8006/orders/   -H "Content-Type: application/json"   -d '{"customer_id":1,"payment_method":"COD","shipping_method":"STANDARD","shipping_address":"123 Nguyen Trai, HCM"}'
```

### 6. Tạo review
```bash
curl -X POST http://localhost:8010/reviews/   -H "Content-Type: application/json"   -d '{"customer_id":1,"book_id":1,"rating":5,"comment":"Rat huu ich"}'
```

### 7. Xem catalog có lọc
```bash
curl "http://localhost:8007/catalog/books/?keyword=clean&in_stock=true&sort=rating_desc"
```

### 8. Gợi ý sách
```bash
curl http://localhost:8011/recommendations/1/
```

### 9. Dashboard manager
```bash
curl http://localhost:8005/manager/dashboard/
```

## Gateway web

- Home: http://localhost:8000/
- Manage books: http://localhost:8000/books/
- Browse catalog: http://localhost:8000/catalog/
- Create customers: http://localhost:8000/customers/
- Cart customer 1: http://localhost:8000/cart/1/
- Orders customer 1: http://localhost:8000/orders/1/
- Reviews book 1: http://localhost:8000/reviews/1/
- Recommendations customer 1: http://localhost:8000/recommendations/1/
- Dashboard: http://localhost:8000/dashboard/

## Gợi ý tiếp theo nếu muốn hoàn thiện hơn Assignment 05

1. Thêm `manager-service` quyền duyệt collection của `catalog-service`.
2. Tách auth đơn giản cho staff và manager.
3. Thêm test tự động bằng Django test hoặc pytest.
4. Thêm sơ đồ kiến trúc và API docs để nộp.
5. Khi lên Assignment 06 thì đổi order workflow sang Saga + message broker + JWT.
