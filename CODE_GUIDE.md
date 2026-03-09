# Code Guide - BookStore Microservice Assignment 05

Tài liệu này giải thích cách code toàn bộ project Stage 3 theo đúng hướng appendix: mỗi service là một Django project riêng, giao tiếp qua REST, chạy bằng `docker compose`.

## 1. Tư duy triển khai

Mỗi service đều có cùng một khung:

```text
service-name/
  manage.py
  requirements.txt
  Dockerfile
  service_package/
    settings.py
    urls.py
    asgi.py
    wsgi.py
  app/
    models.py
    serializers.py
    views.py
    urls.py
    migrations/
```

Ý tưởng chính:
- `models.py`: dữ liệu riêng của service
- `serializers.py`: validate dữ liệu vào ra
- `views.py`: REST API + gọi sang service khác nếu cần
- `urls.py`: khai báo endpoint
- `Dockerfile`: chạy migrate rồi start server

## 2. Service và trách nhiệm

### customer-service
Giữ thông tin customer.
Khi `POST /customers/` thành công thì gọi sang `cart-service` để tự tạo cart.

### book-service
Giữ dữ liệu sách.
Có thêm 2 API quan trọng cho order flow:
- `POST /books/<id>/reserve/`
- `POST /books/<id>/release/`

### cart-service
Giữ cart và cart item.
Khi thêm item, service gọi `book-service` để chắc chắn sách tồn tại và còn đủ stock.

### staff-service
Là lớp proxy cho staff quản lý sách.
Nó chuyển request CRUD sang `book-service`.

### manager-service
Tổng hợp dashboard và health status của nhiều service.
Dùng cho demo và báo cáo.

### order-service
Tạo order từ cart.
Flow:
1. đọc cart từ `cart-service`
2. đọc sách từ `book-service`
3. reserve stock
4. reserve payment ở `pay-service`
5. reserve shipment ở `ship-service`
6. confirm payment + shipment
7. clear cart

### catalog-service
Cho customer duyệt catalog theo từ khóa, giá, stock, rating.
Nó đọc sách từ `book-service` và rating từ `comment-rate-service`.

### pay-service
Lưu payment reservation và confirm/cancel payment.

### ship-service
Lưu shipment reservation và confirm/cancel shipment.

### comment-rate-service
Cho customer review sách.
Validate cả `customer_id` và `book_id` trước khi tạo review.

### recommender-ai-service
Bản đơn giản theo kiểu academic demo.
Nó gợi ý sách bằng cách lấy danh sách sách từ `book-service`, review summary từ `comment-rate-service`, rồi xếp hạng theo rating + số review + stock.

### api-gateway
Tạo web interface để demo nhanh.
Không chứa logic nghiệp vụ chính.
Chỉ đóng vai trò gọi API từ các service khác.

## 3. File quan trọng nhất nên đọc theo thứ tự

1. `customer-service/app/views.py`
2. `cart-service/app/views.py`
3. `book-service/app/views.py`
4. `order-service/app/views.py`
5. `pay-service/app/views.py`
6. `ship-service/app/views.py`
7. `comment-rate-service/app/views.py`
8. `catalog-service/app/views.py`
9. `recommender-ai-service/app/views.py`
10. `api-gateway/app/views.py`
11. `docker-compose.yml`

## 4. Endpoint cốt lõi cho demo

### Customer + cart
- `POST /customers/`
- `GET /customers/`
- `POST /carts/`
- `GET /carts/<customer_id>/`
- `POST /cart-items/`
- `DELETE /carts/<customer_id>/clear/`

### Book + staff
- `GET /books/`
- `POST /books/`
- `PUT/PATCH/DELETE /books/<id>/`
- `POST /books/<id>/reserve/`
- `POST /books/<id>/release/`
- `GET /staff/books/`
- `POST /staff/books/`

### Order + payment + shipping
- `POST /orders/`
- `GET /orders/customer/<customer_id>/`
- `POST /payments/reserve/`
- `POST /payments/<id>/confirm/`
- `POST /shipments/reserve/`
- `POST /shipments/<id>/confirm/`

### Review + catalog + recommendation
- `POST /reviews/`
- `GET /reviews/book/<book_id>/`
- `GET /reviews/book/<book_id>/summary/`
- `GET /catalog/books/`
- `GET /recommendations/<customer_id>/`

## 5. Vì sao order-service phải giữ snapshot dữ liệu sách

Trong `OrderItem` có:
- `title_snapshot`
- `price_snapshot`

Lý do:
Sau khi order đã tạo, nếu staff sửa tên sách hoặc giá trong `book-service`, order cũ vẫn phải giữ đúng dữ liệu tại thời điểm mua.

## 6. Cách giải thích trong báo cáo

Khi viết report, bạn có thể mô tả như sau:
- `customer-service`: bounded context Customer
- `book-service`: bounded context Book
- `cart-service`: bounded context Shopping Cart
- `order-service`: bounded context Ordering
- `pay-service`: bounded context Payment
- `ship-service`: bounded context Shipping
- `comment-rate-service`: bounded context Review
- `catalog-service`: bounded context Catalog/Browsing
- `recommender-ai-service`: bounded context Recommendation

## 7. Những gì còn có thể nâng cấp

Đây là bản phù hợp Assignment 05. Để lên Assignment 06, bạn có thể nâng cấp:
- thay REST đồng bộ trong order workflow bằng Saga
- thêm auth-service với JWT
- thêm RabbitMQ hoặc Kafka
- thêm centralized logging, metrics, health checks sâu hơn
- thêm RBAC cho staff và manager

## 8. Demo sequence khuyến nghị

1. tạo staff
2. tạo book bằng staff-service
3. tạo customer
4. customer được auto-create cart
5. add item vào cart
6. review sách
7. xem catalog có rating
8. tạo order với payment + shipping
9. kiểm tra cart đã rỗng, stock đã giảm
10. mở dashboard manager

## 9. Chỗ bạn nên chỉnh nếu thầy muốn khác

Nếu thầy muốn bài “đúng nghĩa microservice hơn” thì bạn chỉnh ở đây:
- thêm database khác ngoài SQLite
- thêm auth token
- thêm retry/timeout/circuit breaker
- thêm swagger hoặc Postman collection
- thêm test cases cho từng service
