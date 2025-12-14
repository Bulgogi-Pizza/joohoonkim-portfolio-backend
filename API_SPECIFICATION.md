# Backend API Specification for Joohoon Kim Portfolio Site

## Base URL
- Production: `https://api.joohoonkim.site`
- Development: `http://localhost:8000`

## Authentication
All admin endpoints require authentication using HTTP-only cookies.

### Session Cookie
- Name: `session` or custom
- HttpOnly: `true`
- Secure: `true` (production only)
- SameSite: `Lax` or `Strict`

---

## 1. Authentication APIs

### 1.1 Login
```http
POST /api/auth/login
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "admin",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "admin": true,
  "username": "admin"
}
```

**Response (401 Unauthorized):**
```json
{
  "success": false,
  "message": "Invalid credentials"
}
```

**Note:** Sets HTTP-only session cookie in response

---

### 1.2 Logout
```http
POST /api/auth/logout
```

**Response (200 OK):**
```json
{
  "success": true
}
```

**Note:** Clears session cookie

---

### 1.3 Check Authentication
```http
GET /api/auth/me
```

**Response (200 OK - Authenticated):**
```json
{
  "admin": true,
  "username": "admin"
}
```

**Response (200 OK - Not Authenticated):**
```json
{
  "admin": false
}
```

---

## 2. Publications APIs

### 2.1 List Publications
```http
GET /api/publications
Query Parameters:
  - status: "published" | "in_revision" (optional)
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "number": 10,
    "title": "Wide-field-of-view, switchable, multi-dimensional light-field display using a metasurface lenticular lens",
    "authors": "J. Kim, et al.",
    "journal": "Nature",
    "volume": "22",
    "pages": "474-481",
    "year": "2025",
    "status": "published",
    "featured_info": "Featured in Nature News",
    "doi": "10.1038/s41563-023-01485-5",
    "arxiv": "https://arxiv.org/abs/example",
    "image_path": "https://s3.amazonaws.com/bucket/publications/image1.jpg",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### 2.2 Get Publication Years
```http
GET /api/publications/years
```

**Response (200 OK):**
```json
{
  "years": ["2025", "2024", "2023", "2022"]
}
```

---

### 2.3 Create Publication (Admin)
```http
POST /api/publications
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:**
```json
{
  "number": 11,
  "title": "Publication Title",
  "authors": "Author Names",
  "journal": "Journal Name",
  "volume": "23",
  "pages": "100-120",
  "year": "2025",
  "status": "published",
  "featured_info": "Award winning",
  "doi": "10.1234/example",
  "arxiv": "https://arxiv.org/abs/xxxx"
}
```

**Response (201 Created):**
```json
{
  "id": 11,
  "number": 11,
  "title": "Publication Title",
  ...
}
```

---

### 2.4 Update Publication (Admin)
```http
PUT /api/publications/{id}
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:** Same as Create

**Response (200 OK):** Updated publication object

---

### 2.5 Delete Publication (Admin)
```http
DELETE /api/publications/{id}
Authorization: Required (Session Cookie)
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Publication deleted"
}
```

---

## 3. Research Highlights APIs

### 3.1 List Research Highlights
```http
GET /api/research-highlights
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "image_path": "https://s3.amazonaws.com/bucket/highlights/image1.jpg",
    "link": "/publications",
    "description": "Featured in Nature News",
    "alt_text": "Research highlight description",
    "order_index": 1,
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### 3.2 Create Research Highlight (Admin)
```http
POST /api/research-highlights
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:**
```json
{
  "image_path": "https://s3.amazonaws.com/bucket/highlights/image.jpg",
  "link": "/publications",
  "description": "Featured in Nature News",
  "alt_text": "Image description",
  "order_index": 1,
  "is_active": true
}
```

**Response (201 Created):** Created object

---

### 3.3 Update Research Highlight (Admin)
```http
PUT /api/research-highlights/{id}
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:** Same as Create

**Response (200 OK):** Updated object

---

### 3.4 Delete Research Highlight (Admin)
```http
DELETE /api/research-highlights/{id}
Authorization: Required (Session Cookie)
```

**Response (200 OK):**
```json
{
  "success": true
}
```

---

### 3.5 Upload Research Highlight Image (Admin)
```http
POST /api/research-highlights/upload-image
Content-Type: multipart/form-data
Authorization: Required (Session Cookie)
```

**Request Body:**
```
file: <image file>
```

**Response (200 OK):**
```json
{
  "image_path": "https://s3.amazonaws.com/bucket/highlights/abc123.jpg"
}
```

**Note:** Upload to S3 and return full URL

---

## 4. Representative Works APIs

### 4.1 List Representative Works
```http
GET /api/representative-works
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "High-Efficiency Metasurface",
    "journal": "Nature Materials",
    "volume": "22",
    "pages": "100-110",
    "year": "2023",
    "is_in_revision": false,
    "image_path": "https://s3.amazonaws.com/bucket/works/image1.jpg",
    "order_index": 1,
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### 4.2 Create Representative Work (Admin)
```http
POST /api/representative-works
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:**
```json
{
  "title": "Work Title",
  "journal": "Journal Name",
  "volume": "22",
  "pages": "100-110",
  "year": "2023",
  "is_in_revision": false,
  "image_path": "https://s3.amazonaws.com/bucket/works/image.jpg",
  "order_index": 1,
  "is_active": true
}
```

**Response (201 Created):** Created object

---

### 4.3 Update Representative Work (Admin)
```http
PUT /api/representative-works/{id}
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:** Same as Create

**Response (200 OK):** Updated object

---

### 4.4 Delete Representative Work (Admin)
```http
DELETE /api/representative-works/{id}
Authorization: Required (Session Cookie)
```

**Response (200 OK):**
```json
{
  "success": true
}
```

---

### 4.5 Upload Representative Work Image (Admin)
```http
POST /api/representative-works/upload-image
Content-Type: multipart/form-data
Authorization: Required (Session Cookie)
```

**Request Body:**
```
file: <image file>
```

**Response (200 OK):**
```json
{
  "image_path": "https://s3.amazonaws.com/bucket/works/abc123.jpg"
}
```

---

## 5. Cover Arts APIs

### 5.1 List Cover Arts
```http
GET /api/cover-arts
Query Parameters:
  - active_only: 1 (optional, returns only is_active=true)
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "image_path": "https://s3.amazonaws.com/bucket/covers/image1.jpg",
    "link": "https://doi.org/10.1234/example",
    "journal": "Nature Materials",
    "volume": "22",
    "year": "2023",
    "description": "Cover art description",
    "alt_text": "Cover art alt text",
    "order_index": 1,
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### 5.2 Create Cover Art (Admin)
```http
POST /api/cover-arts
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:**
```json
{
  "image_path": "https://s3.amazonaws.com/bucket/covers/image.jpg",
  "link": "https://doi.org/10.1234/example",
  "journal": "Nature Materials",
  "volume": "22",
  "year": "2023",
  "description": "Cover art description",
  "alt_text": "Alt text",
  "order_index": 1,
  "is_active": true
}
```

**Response (201 Created):** Created object

---

### 5.3 Update Cover Art (Admin)
```http
PUT /api/cover-arts/{id}
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:** Same as Create

**Response (200 OK):** Updated object

---

### 5.4 Delete Cover Art (Admin)
```http
DELETE /api/cover-arts/{id}
Authorization: Required (Session Cookie)
```

**Response (200 OK):**
```json
{
  "success": true
}
```

---

### 5.5 Upload Cover Art Image (Admin)
```http
POST /api/cover-arts/upload-image
Content-Type: multipart/form-data
Authorization: Required (Session Cookie)
```

**Request Body:**
```
file: <image file>
```

**Response (200 OK):**
```json
{
  "image_path": "https://s3.amazonaws.com/bucket/covers/abc123.jpg"
}
```

---

## 6. Research Areas APIs

### 6.1 List Research Areas
```http
GET /api/research-areas
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Nanophotonics",
    "slug": "nanophotonics",
    "icon_path": "https://s3.amazonaws.com/bucket/icons/nanophotonics.png",
    "description": "## Nanophotonics\n\nStudy of light at the nanoscale...",
    "order_index": 1,
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### 6.2 Get Research Area by Slug
```http
GET /api/research-areas/{slug}
```

**Response (200 OK):** Single research area object

**Response (404 Not Found):**
```json
{
  "error": "Research area not found"
}
```

---

### 6.3 Create Research Area (Admin)
```http
POST /api/research-areas
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:**
```json
{
  "title": "Nanophotonics",
  "slug": "nanophotonics",
  "icon_path": "https://s3.amazonaws.com/bucket/icons/icon.png",
  "description": "## Nanophotonics\n\nDetailed description with markdown...",
  "order_index": 1,
  "is_active": true
}
```

**Response (201 Created):** Created object

---

### 6.4 Update Research Area (Admin)
```http
PUT /api/research-areas/{id}
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:** Same as Create

**Response (200 OK):** Updated object

---

### 6.5 Delete Research Area (Admin)
```http
DELETE /api/research-areas/{id}
Authorization: Required (Session Cookie)
```

**Response (200 OK):**
```json
{
  "success": true
}
```

---

### 6.6 Upload Research Area Icon (Admin)
```http
POST /api/research-areas/upload-icon
Content-Type: multipart/form-data
Authorization: Required (Session Cookie)
```

**Request Body:**
```
file: <image file>
```

**Response (200 OK):**
```json
{
  "icon_path": "https://s3.amazonaws.com/bucket/icons/abc123.png"
}
```

---

### 6.7 Upload Research Area Content Image (Admin)
```http
POST /api/research-areas/upload-content-image
Content-Type: multipart/form-data
Authorization: Required (Session Cookie)
```

**Request Body:**
```
file: <image file>
```

**Response (200 OK):**
```json
{
  "image_path": "https://s3.amazonaws.com/bucket/research-areas/abc123.jpg"
}
```

**Note:** Used for embedding images in markdown description

---

## 7. Media APIs

### 7.1 List Media
```http
GET /api/media
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Breakthrough in Metasurface Manufacturing",
    "source": "Science Daily",
    "date": "2023-04-15",
    "category": "news",
    "url": "https://www.sciencedaily.com/article",
    "image_url": "https://s3.amazonaws.com/bucket/media/image1.jpg",
    "description": "Researchers develop a new method...",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### 7.2 Create Media (Admin)
```http
POST /api/media
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:**
```json
{
  "title": "Media Title",
  "source": "Source Name",
  "date": "2023-04-15",
  "category": "news",
  "url": "https://example.com",
  "image_url": "https://s3.amazonaws.com/bucket/media/image.jpg",
  "description": "Description text"
}
```

**Response (201 Created):** Created object

---

### 7.3 Update Media (Admin)
```http
PUT /api/media/{id}
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:** Same as Create

**Response (200 OK):** Updated object

---

### 7.4 Delete Media (Admin)
```http
DELETE /api/media/{id}
Authorization: Required (Session Cookie)
```

**Response (200 OK):**
```json
{
  "success": true
}
```

---

### 7.5 Upload Media Image (Admin)
```http
POST /api/media/upload-image
Content-Type: multipart/form-data
Authorization: Required (Session Cookie)
```

**Request Body:**
```
file: <image file>
```

**Response (200 OK):**
```json
{
  "image_path": "https://s3.amazonaws.com/bucket/media/abc123.jpg"
}
```

---

## 8. Conferences APIs

### 8.1 List Conferences
```http
GET /api/conferences
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "conference_name": "CLEO 2024",
    "location": "Charlotte, USA",
    "date": "2024-05-05",
    "presentation_type": "Oral",
    "award": "Best Student Paper",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### 8.2 Create Conference (Admin)
```http
POST /api/conferences
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:**
```json
{
  "conference_name": "CLEO 2024",
  "location": "Charlotte, USA",
  "date": "2024-05-05",
  "presentation_type": "Oral",
  "award": "Best Student Paper"
}
```

**Response (201 Created):** Created object

---

### 8.3 Update Conference (Admin)
```http
PUT /api/conferences/{id}
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:** Same as Create

**Response (200 OK):** Updated object

---

### 8.4 Delete Conference (Admin)
```http
DELETE /api/conferences/{id}
Authorization: Required (Session Cookie)
```

**Response (200 OK):**
```json
{
  "success": true
}
```

---

## 9. Awards APIs

### 9.1 List Awards
```http
GET /api/awards
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Presidential Science Fellowship",
    "organization": "Government of Korea",
    "details": "Ph.D.",
    "year": "2024",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### 9.2 Create Award (Admin)
```http
POST /api/awards
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:**
```json
{
  "title": "Award Title",
  "organization": "Organization Name",
  "details": "Details",
  "year": "2024"
}
```

**Response (201 Created):** Created object

---

### 9.3 Update Award (Admin)
```http
PUT /api/awards/{id}
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:** Same as Create

**Response (200 OK):** Updated object

---

### 9.4 Delete Award (Admin)
```http
DELETE /api/awards/{id}
Authorization: Required (Session Cookie)
```

**Response (200 OK):**
```json
{
  "success": true
}
```

---

## 10. Hero Section API

### 10.1 Get Hero Content
```http
GET /api/hero
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Innovating",
  "title_highlight": "Nanophotonics",
  "description": "Ph.D. student at POSTECH...",
  "cta_primary_text": "Explore Research",
  "cta_primary_link": "/research",
  "cta_secondary_text": "View CV",
  "cta_secondary_link": "/cv",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

### 10.2 Update Hero Content (Admin)
```http
PUT /api/hero
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:**
```json
{
  "title": "Innovating",
  "title_highlight": "Nanophotonics",
  "description": "Ph.D. student at POSTECH...",
  "cta_primary_text": "Explore Research",
  "cta_primary_link": "/research",
  "cta_secondary_text": "View CV",
  "cta_secondary_link": "/cv"
}
```

**Response (200 OK):** Updated object

---

## 11. Education APIs

### 11.1 List Education
```http
GET /api/education
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "degree": "M.S./Ph.D. in Mechanical Engineering",
    "university": "POSTECH",
    "country": "Korea",
    "from": "2021",
    "to": "2026, expected",
    "order_index": 1,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### 11.2 Create Education (Admin)
```http
POST /api/education
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:**
```json
{
  "degree": "M.S./Ph.D. in Mechanical Engineering",
  "university": "POSTECH",
  "country": "Korea",
  "from": "2021",
  "to": "2026, expected",
  "order_index": 1
}
```

**Response (201 Created):** Created object

---

### 11.3 Update Education (Admin)
```http
PUT /api/education/{id}
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:** Same as Create

**Response (200 OK):** Updated object

---

### 11.4 Delete Education (Admin)
```http
DELETE /api/education/{id}
Authorization: Required (Session Cookie)
```

**Response (200 OK):**
```json
{
  "success": true
}
```

---

## 12. Experience APIs

### 12.1 List Experience
```http
GET /api/experience
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "role": "Visiting Researcher",
    "institution": "Plant and Food Research",
    "location": "New Zealand",
    "period": "2023",
    "description": "Host: Dr. Jonghyun Choi",
    "order_index": 1,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### 12.2 Create Experience (Admin)
```http
POST /api/experience
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:**
```json
{
  "role": "Visiting Researcher",
  "institution": "Plant and Food Research",
  "location": "New Zealand",
  "period": "2023",
  "description": "Host: Dr. Jonghyun Choi",
  "order_index": 1
}
```

**Response (201 Created):** Created object

---

### 12.3 Update Experience (Admin)
```http
PUT /api/experience/{id}
Content-Type: application/json
Authorization: Required (Session Cookie)
```

**Request Body:** Same as Create

**Response (200 OK):** Updated object

---

### 12.4 Delete Experience (Admin)
```http
DELETE /api/experience/{id}
Authorization: Required (Session Cookie)
```

**Response (200 OK):**
```json
{
  "success": true
}
```

---

## Image Upload Requirements

### S3 Upload Configuration

All image uploads should:

1. **Upload to S3**: Store files in AWS S3 or compatible object storage
2. **Return Full URL**: Always return the complete URL with https://
3. **Public Access**: Images should be publicly accessible (no authentication required)
4. **File Name**: Use unique file names (UUID or timestamp-based)
5. **Accepted Formats**: JPG, PNG, GIF, WebP
6. **Max File Size**: Recommended 10MB per file
7. **Image Optimization**: Optionally optimize/compress before storing

### S3 Bucket Structure (Recommended)
```
bucket-name/
├── publications/
├── highlights/
├── works/
├── covers/
├── icons/
├── media/
└── research-areas/
```

### Example Upload Response
```json
{
  "image_path": "https://s3.amazonaws.com/joohoon-portfolio/covers/a1b2c3d4-e5f6-7890.jpg"
}
```

Or with CloudFront CDN:
```json
{
  "image_path": "https://d123456789.cloudfront.net/covers/a1b2c3d4-e5f6-7890.jpg"
}
```

---

## CORS Configuration

Frontend domains that need access:
- `https://dev.d1jx5u7u0ebuxt.amplifyapp.com` (dev)
- `https://joohoonkim.site` (production)
- `http://localhost:3000` (local development)

Required CORS headers:
```
Access-Control-Allow-Origin: <frontend-domain>
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type
Access-Control-Allow-Credentials: true
```

---

## Error Responses

### Standard Error Format
```json
{
  "error": "Error message",
  "details": "Additional details (optional)"
}
```

### Common HTTP Status Codes
- `200 OK`: Successful GET, PUT, DELETE
- `201 Created`: Successful POST
- `400 Bad Request`: Invalid request body or parameters
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

---

## Database Schema Recommendations

### Common Fields for All Tables
- `id`: Primary key (auto-increment)
- `created_at`: Timestamp, default CURRENT_TIMESTAMP
- `updated_at`: Timestamp, auto-update on modification

### Indexes
- Create indexes on frequently queried fields: `slug`, `year`, `is_active`, `order_index`
- Create indexes on foreign keys

---

## Additional Notes

1. **Ordering**: Results should be ordered by `order_index` ASC for items with this field
2. **Filtering**: Active-only filtering should be applied where `is_active` field exists
3. **Markdown**: The `description` field in research areas supports Markdown formatting
4. **Date Format**: Use ISO 8601 format (YYYY-MM-DD) for dates
5. **Slugs**: Should be lowercase, alphanumeric with hyphens only
6. **Numbers**: Publication numbers should be unique and typically descending (newest = highest)

---

## Testing Endpoints

Use these tools for testing:
- Postman
- curl
- HTTPie
- Insomnia

Example curl test:
```bash
# Test login
curl -X POST https://api.joohoonkim.site/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}' \
  -c cookies.txt

# Test authenticated request
curl -X GET https://api.joohoonkim.site/api/publications \
  -b cookies.txt
```

---

## Version
API Version: 1.0  
Last Updated: 2024-12-14

