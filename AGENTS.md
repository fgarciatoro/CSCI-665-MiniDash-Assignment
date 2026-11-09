# AI Assistant Rules (AGENTS.md)

**Language / Stack:** Python with FastAPI and SQLite
**Test Framework:** pytest

**Conventions:**
1. **Layered Architecture:** Maintain the existing layered structure separating routes, services, and the repository layer
2. **Small, Testable Slices:** Implement features in small, reviewable slices where every piece of logic is verified by automated tests 
3. **Security & Privacy:** Never include secrets, API keys, or personal data in the code or prompts
