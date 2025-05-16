# Medol AI Lab Test

## Запуск

```bah
docker compose up
```

# Примеры запросов

### Получение JWT-токена

Запрос:

```bash
curl -X 'POST' \
  'http://localhost:8080/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=admin&password=tW.Oj%2B-()iGEf~GE'
```

Ответ:

```bash
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc0NzMyOTIyOH0.meProey9KdvGNaEhIMh47GUGYP4sKR_v2z8yEtIMpTs",
  "token_type": "bearer"
}
```

`access_token` и есть JWT-токен.

### Использование JWT-токена в запросах

Запрос:

```bash
curl -X 'GET' \
  'http://localhost:8080/users/me' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc0NzMyOTIyOH0.meProey9KdvGNaEhIMh47GUGYP4sKR_v2z8yEtIMpTs'
```

В теле запроса должен обязательно присутствовать заголовок `Authorization: Bearer <JWT-токен>`

Ответ:

```bash
{
  "username": "admin"
}
```

В данном примере `/users/me` возвращает имя текущего пользователя по его JWT-токену.

### Загрузка файлов через /upload

Запрос:

```bash
curl -X 'POST' \
  'http://localhost:8080/upload' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc0NzMyOTIyOH0.meProey9KdvGNaEhIMh47GUGYP4sKR_v2z8yEtIMpTs' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@Anonymized_20250514 (1) — копия.dcm'
```

В теле запроса должны обязательно присутствовать:

* заголовок `Content-Type: multipart/form-data`

* сам файл через флаг `cURL` `-F`: `'file=@<файл>'`, где `файл` является путём к файлу.

В случае успешной загрузки файла в MinIO будет выдан ответ:

```bash
{
  "id": "a400ad33-15b2-4756-b7d4-d5d9ecc19b72",
  "filename": "Anonymized_20250514 (1) — копия.dcm"
}
```

В ответе `id` является UUID-идентификатором файла.

`filename` же является именем файла в MinIO.

### Как скачать файл через /download

```bash
curl -X 'GET' \
  'http://localhost:8080/download/7a0d9f5c-4552-455b-b87e-b72fac29ba16' \
  --output "primer.dcm" \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc0NzM2NjU4MX0.xwnzV7q_DA_Nht6ygMSJpilR7qzPEo6O_TvMHfeQx1Q'
```

Параметром `download/` является UUID-файла, полученный в [Загрузка файлов через /upload](#Загрузка файлов через /upload).

### Как получить список всех доступных файлов

```bash
curl -X 'GET' \
  'http://localhost:8080/files' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc0NzM2NjU4MX0.xwnzV7q_DA_Nht6ygMSJpilR7qzPEo6O_TvMHfeQx1Q'
```

Ответом будет являться список всех файлов:

```json
[
  {
    "id": "7a0d9f5c-4552-455b-b87e-b72fac29ba16",
    "filename": "Anonymized_20250514.dcm"
  },
  {
    "id": "c371876a-aa81-4520-ab6b-6981f15d2044",
    "filename": "Anonymized_20250514 (1).dcm"
  },
  {
    "id": "a400ad33-15b2-4756-b7d4-d5d9ecc19b72",
    "filename": "Anonymized_20250514 (1) — копия.dcm"
  },
  {
    "id": "1e174807-921d-4d2f-a81d-bcf868f1c544",
    "filename": "Anonymized_20250514 (3).dcm"
  }
]
```

