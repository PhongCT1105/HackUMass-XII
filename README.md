# SyntheSearch

### Authors  
**Phong Cao, Hien Hoang, Doanh Phung, Minh Bui**

**Start server (backend):**

`cd backend`

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirement.txt` (ios => make sure there's no pywin32 in requirement.txt)

`uvicorn main:app --reload`

**Start client (frontend):**

`cd frontend`

`npm i`

`npm run dev`
