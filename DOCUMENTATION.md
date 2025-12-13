markdown
# Reading Time API - Documentation

**Base URL:** `{https://reading-time-api.onrender.com}`

**Authentication:** Include your API Key in the header:
`X-API-Key: YOUR_API_KEY_HERE`

## Endpoints

### Health Check
**`GET /api/reading-time/health/`**
*No API key needed.*

**Response:**
```json
{"service": "Reading Time API", "status": "operational"}
Single Text Calculation
GET /api/reading-time/

Parameters:

text (required): Your text.

wpm (optional): Words per minute. Default: 250.

Example:
GET {https://reading-time-api.onrender.com}/api/reading-time/?text=Sample%20text&wpm=250

Response:

json
{"status": "success", "data": {"minutes": 1, "word_count": 1, "display": "1 min"}}
Bulk Calculation
POST /api/reading-time/bulk/

Request Body (JSON):

json
{"texts": ["Text one", "Text two"], "wpm": 250}
Support: Contact via your Gumroad purchase email.
