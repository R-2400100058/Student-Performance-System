# 🔌 API Documentation

## Base URL
```
http://localhost:8000/analytics/api/
http://localhost:8000/accounts/
```

---

## Students API

### Get All Students
**Endpoint:** `GET /analytics/api/students/`

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "roll_no": "STU001",
    "department": "Science"
  }
]
```

---

### Create Student
**Endpoint:** `POST /analytics/api/students/create/`

**Request Body:**
```json
{
  "name": "John Doe",
  "roll_no": "STU001",
  "department": "Science"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Student created successfully",
  "student": {
    "id": 1,
    "name": "John Doe",
    "roll_no": "STU001",
    "department": "Science"
  }
}
```

**Validations:**
- Name: Required, max 100 characters
- Roll No: Required, max 20 characters
- Department: Required, max 100 characters

---

### Update Student
**Endpoint:** `POST /analytics/api/students/<id>/update/`

**Request Body:**
```json
{
  "name": "Jane Doe",
  "roll_no": "STU001",
  "department": "Science"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Student updated successfully",
  "student": {
    "id": 1,
    "name": "Jane Doe",
    "roll_no": "STU001",
    "department": "Science"
  }
}
```

---

### Delete Student
**Endpoint:** `POST /analytics/api/students/<id>/delete/`

**Response:**
```json
{
  "success": true,
  "message": "Student deleted successfully"
}
```

---

## Marks API

### Get All Marks
**Endpoint:** `GET /analytics/api/marks/`

**Response:**
```json
[
  {
    "id": 1,
    "student_id": 1,
    "student_name": "John Doe",
    "student_roll_no": "STU001",
    "subject_id": 1,
    "subject_name": "Mathematics",
    "marks_obtained": 85,
    "attendance_percentage": 90.0
  }
]
```

---

### Create Mark Entry
**Endpoint:** `POST /analytics/api/marks/create/`

**Request Body:**
```json
{
  "student_id": 1,
  "subject_id": 1,
  "marks_obtained": 85,
  "attendance_percentage": 90.0
}
```

**Response:**
```json
{
  "success": true,
  "message": "Mark created successfully",
  "mark": {
    "id": 1,
    "student_id": 1,
    "subject_id": 1,
    "marks_obtained": 85,
    "attendance_percentage": 90.0
  }
}
```

**Validations:**
- Student ID: Required, must exist
- Subject ID: Required, must exist
- Marks: Required, 0-100
- Attendance: Required, 0-100
- Duplicate prevention: (student, subject) pair must be unique

---

### Update Mark Entry
**Endpoint:** `POST /analytics/api/marks/<id>/update/`

**Request Body:**
```json
{
  "marks_obtained": 90,
  "attendance_percentage": 95.0
}
```

**Response:**
```json
{
  "success": true,
  "message": "Mark updated successfully",
  "mark": {
    "id": 1,
    "marks_obtained": 90,
    "attendance_percentage": 95.0
  }
}
```

**Validations:**
- Marks: 0-100 (if provided)
- Attendance: 0-100 (if provided)

---

### Delete Mark Entry
**Endpoint:** `POST /analytics/api/marks/<id>/delete/`

**Response:**
```json
{
  "success": true,
  "message": "Mark deleted successfully"
}
```

---

## Subjects API

### Get All Subjects
**Endpoint:** `GET /analytics/api/subjects/`

**Response:**
```json
[
  {
    "id": 1,
    "subject_name": "Mathematics"
  },
  {
    "id": 2,
    "subject_name": "Science"
  }
]
```

---

### Create Subject
**Endpoint:** `POST /analytics/api/subjects/create/`

**Request Body:**
```json
{
  "subject_name": "English"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Subject created successfully",
  "subject": {
    "id": 3,
    "subject_name": "English"
  }
}
```

**Validations:**
- Subject Name: Required, max 100 characters
- Unique: Subject names should be unique

---

## Dashboard API

### Get Dashboard Statistics
**Endpoint:** `GET /analytics/api/dashboard-stats/`

**Response:**
```json
{
  "total_students": 50,
  "average_score": 75.50,
  "attendance": 88.20,
  "pass_rate": 92.50,
  "total_marks": 150
}
```

---

### Get Performance Trend Data
**Endpoint:** `GET /analytics/api/performance-data/`

**Response:**
```json
{
  "labels": ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"],
  "data": [65, 69, 72, 75, 77, 78]
}
```

---

### Get Subject Comparison Data
**Endpoint:** `GET /analytics/api/subject-data/`

**Response:**
```json
{
  "labels": ["Mathematics", "Science", "English", "History", "Geography"],
  "data": [82, 75, 88, 70, 79]
}
```

---

## Error Handling

### Error Response Format
```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

### Common Error Messages
- `"Student name cannot be empty"` - Validation error
- `"Marks must be between 0 and 100"` - Range validation
- `"Mark entry already exists"` - Duplicate prevention
- `"Please fill all fields"` - Missing required field

---

## Authentication

All API endpoints require the user to be logged in. The application uses Django's session-based authentication.

**CSRF Protection:** All POST requests must include the CSRF token in headers:
```javascript
'X-CSRFToken': csrftoken
```

---

## Rate Limiting
Currently no rate limiting is implemented. In production, consider adding:
- Django Ratelimit
- Django REST Framework throttling

---

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request / Validation Error |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Server Error |

---

## Example Usage (JavaScript/Fetch)

### Create Student
```javascript
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

fetch('/analytics/api/students/create/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken,
  },
  body: JSON.stringify({
    name: 'John Doe',
    roll_no: 'STU001',
    department: 'Science'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Add Marks
```javascript
fetch('/analytics/api/marks/create/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken,
  },
  body: JSON.stringify({
    student_id: 1,
    subject_id: 1,
    marks_obtained: 85,
    attendance_percentage: 90
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Get All Marks
```javascript
fetch('/analytics/api/marks/')
  .then(response => response.json())
  .then(marks => console.log(marks));
```

---

## Database Models

### Student Model
```python
class Student(models.Model):
    name: CharField(max_length=100)
    roll_no: CharField(max_length=20)
    department: CharField(max_length=100)
```

### Subject Model
```python
class Subject(models.Model):
    subject_name: CharField(max_length=100)
```

### Mark Model
```python
class Mark(models.Model):
    student: ForeignKey(Student)
    subject: ForeignKey(Subject)
    marks_obtained: IntegerField
    attendance_percentage: FloatField
```

### Profile Model (Accounts)
```python
class Profile(models.Model):
    user: OneToOneField(User)
    gender: CharField(choices=['Male', 'Female', 'Other'])
    role: CharField(choices=['Student', 'Teacher', 'Admin'])
    created_at: DateTimeField
    updated_at: DateTimeField
```

---

## Performance Considerations

1. **Indexing**: Consider adding indexes on frequently queried fields
2. **Pagination**: Add pagination for large datasets
3. **Caching**: Cache dashboard statistics
4. **Query Optimization**: Use `select_related()` and `prefetch_related()` where appropriate

---

## Security Considerations

1. ✅ CSRF Protection enabled
2. ✅ Authentication required on all endpoints
3. ✅ Input validation on all fields
4. ✅ Input sanitization
5. ⚠️ Consider adding: Rate limiting, API key authentication, CORS headers

---

## Future Enhancements

- [ ] REST Framework with serializers
- [ ] Advanced filtering and searching
- [ ] Bulk operations
- [ ] Export to CSV/PDF
- [ ] API documentation with Swagger/OpenAPI
- [ ] GraphQL API
- [ ] WebSocket for real-time updates
