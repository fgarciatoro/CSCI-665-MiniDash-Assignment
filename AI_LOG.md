AI usage log.

Template from Appendix B:

| Field                            | Your entry (example from a Track A student)|
|------------                      |-----|
| Entry # / date                   |   4 / Oct 21, 7:40 pm  |
| Tool, model, mode                | GitHub Copilot, agent mode (auto model)|
| Slice                            | Slice 3: domain rule validate_schedule()|
| Prompt (verbatim or summarized)  | Pasted the contract and three boundary examples (44, 45, 46 minutes) from requirements.md. Asked for the function and tests only, no new dependencies,only files in /src/orders.  |
| What the AI produced     | The function and four tests. It called datetime.now() directly and also added a helper module I did not request. |
| What I verified | Ran pytest (all passed, but tests used the real clock). Read the full diff. Mutation check: changed 45 to 44 in the rule and a test failed, as expected. |
| What I changed and why | Injected a clock parameter so tests are deterministic. Deleted the unrequested helper module (scope creep).|
| Outcome | Modified, then accepted. Committed as “Add 45-minute lead-time rule (AI-assisted, clock injected)”.|

*** Start of Entries ***

| Field                            | Your entry|
|------------                      |-----|
| Entry # / date                   |   0 / Nov 9, 1:40 am  |
| Tool, model, mode                | GitHub Copilot, agent mode (auto model)|
| Slice                            | Baseline: Repo creation|
| Prompt (verbatim or summarized)  | Create a small food-delivery REST API called MiniDash in Python with FastAPI and SQLite. Tables: restaurants (id, name, cuisine, opens_at, closes_at, avg_prep_minutes), menu_items (id, restaurant_id, name, price_cents), orders (id, restaurant_id, status, total_cents, address, created_at) and order_items. Endpoints: GET /restaurants, GET /restaurants/{id}/menu, POST /orders, GET /orders/{id}, PATCH /orders/{id}/status. Use a layered structure (routes, services, repository). Seed 5 restaurants. Add pytest tests for each endpoint and a README with run instructions. Do not add authentication or any dependency beyond fastapi, uvicorn, and pytest. (From Appendix C)|
| What the AI produced             | Initial repository, README file, and folder structure |
| What I verified                  | Folder structure and accuracy of files |
| What I changed and why           | Minor formatting edits to some files. Largely accepted as is.|
| Outcome                          | Accepted. Committed as "Baseline: Merge pull request #1|

| Field                            | My entry |
|------------                      |-----|
| Entry # / date                   |   1 / Nov 9,    |
| Tool, model, mode                | GitHub Copilot, agent mode (auto model)|
| Slice                            | Slice 1:|
| Prompt (verbatim or summarized)  | |
| What the AI produced             | |
| What I verified                  | |
| What I changed and why           | |
| Outcome                          | Accepted and committed as "Slice 1: |
