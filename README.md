# Bitespeed-Backend-Assignment 

This project implements an **Identity Reconciliation Service** as described in the Bitespeed Backend Assignment. The goal is to design a backend system that consolidates multiple contact records belonging to the same individual based on shared identifiers such as email and/or phone number.

The service exposes a single `POST /identify` endpoint that accepts an email and/or phone number and determines whether the provided information corresponds to an existing contact. If no match is found, a new primary contact record is created. If a match exists, the system links related record together ensuring older being **primary**, and all subsequent entries become **secondary**

The response returns a combined view of :
- The primary contact ID

- All associated email addresses

- All associated phone numbers

- The list of secondary contact IDs

### Folder Structure 

```
bitespeed-identity/
│
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # DB settings
│   │
│   ├── db.py                # SQLAlchemy engine + session
│   ├── models.py            # Contact model
│   ├── schemas.py           # Pydantic request/response models
│   │
│   ├── services.py          # Identity reconciliation logic
│   └── utils.py             # Normalization helpers
│
├── requirements.txt
├── README.md
└── alembic/ (optional but recommended)
```

### Flow of data/Workflow

```
Client
   │
   ▼
POST /identify
   │
   ▼
FastAPI validates request
   │
   ▼
Call identify_contact()
   │
   ▼
BEGIN TRANSACTION
   │
   ▼
Find contacts by email OR phone
   │
   ├── No matches?
   │       └── Create primary contact
   │
   └── Matches found?
           ├── Determine oldest primary
           ├── Merge if needed
           ├── Insert secondary if new data
   │
   ▼
COMMIT
   │
   ▼
Build consolidated response
   │
   ▼
Return JSON

   ```

