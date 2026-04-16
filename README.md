# Finance Portfolio Analytics API

## Features
Project feature list / requirements following MoSCoW method.

### Must haves
- well structured project
- well thought through DB design with alembic migrations
- auth with jwt (register, login, token refresh, protected endpoints)
    - consider service accounts (may not be relevant for this context)
- testing
    - pytest unit tests (business logic without endpoints or DB)
    - integration tests (endpoint tests with DB using FastAPI's TestClient)
- Docker and Docker Compose
- GitHub Actions (CI/CD)
- proper README (architecture, local setup, API summary, design decisions)

### Should have
- env configs instead of hard coding credentials (pydantic-settings)
- caching with redis
- background price refresh written to DB rather than synchronous to API request
    - can demonstrate a robustness design decision
- structured logging

### Could have
- rate limiting

### Won't have
- Full OAuth2
- Kerbernetes (overkill)
- Graphql (not so much demand)
- websockets (tempting but significantly increases complexity)
- frontend (api docs is my UI)

