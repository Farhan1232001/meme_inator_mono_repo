# Meme-inator Backend

Goal of **Meme-inator** is to provide a cross-platform, social platform for meme sharing, engaging feeds, community interactions, and engagement.

This repository contains a modular-monolithic django-ninja backend built utilizing strict **Clean Architecture** guidelines and **Domain-Driven Design (DDD)** principles, as well as **Object-Oriented Design** principles to maximize maintainability, scalability, and extendability. This architectural goal also helps testability.

## Architectural Overview
The project is conceived and structured around as decoupled modules or context boundaries which are implemented using django apps within the `apps/` directory. Each app follows an isolated 4-layer Clean Architecture pattern.

1. **Domain Layer (`domain/`):** Enterprise rules, pure business domain models, value objects, aggregates, and abstractions (`irepositories`, `iusecases`). Completely devoid of framework/database dependencies.
2. **Application Layer (`application/`):** Orchestration and application use cases (`usecases/`). Handles DTO mapping and controls the flow of domain data.
3. **Infrastructure Layer (`infrastructure/`):** Concrete implementations of external mechanisms (Django DB `models`, caching, message `queues`, concrete `repositories`, and external API `services`).
4. **Delivery Layer (`delivery/` or root views):** Presentation mechanics, exposed API endpoints, and network payloads (REST/JSON controllers).

### Core Components
* **`api/`**: Unified API specs (OpenAPI/YAML for moderation, payments) and base layout wrappers.
* **`core/`**: System-wide cross-cutting concerns including Explicit Dependency Injection mappings (`dependency_injections.py`), Result wrappers (`results.py`), JWT authorization (`jwt_auth.py`), and foundational error schemas.
* **`shared/`**: Generic baseline structures shared across boundaries (e.g., S3 client drivers, SMTP mailers).



## Feature Modules/Apps
**Legend:** 🟢 Completed | 🟡 In Progress | ⚪ Planned / Backlog

- 🟡 **accounts**: Responsible for password management
- 🟢 **app_system**: Responsible for system related stats. In future may handle core settings and configurations. 
- 🟡 **authentication**: Responsible for handling user sessions, token issuance and verification pipelines
- 🟡 **authorization**: Responsible for system permissions (access-control). Also responsible for tracking entitlements which is granted in payments app. Uses django permissions. custom RBAC can be used down the line. 
- 🟡 **commentsections**: Responsible for managing comments and comment_votes (upvote/downvote). 
- 🟢 **feeds**: Responsible for sectional feeds and grid feeds, former is a feed where posts are chunked/sectioned by duration_window, and latter is a normal feed. Sectional feed is used for Popular Today, Popular Monthly, etc. Grid feeds used for Recent, randomized feeds, etc. 
- 🟡 **moderation_sys**: Responsible for creation of particular moderaton cases for particular content (post/comment/etc), responsible for moderation_case submissions, responsible for moderating content via a ModerationProvider (OpenAI Moderation API), and responsible for initiating appeal process. 
- ⚪ **notifications**: Responsible for async notificaton services. Has multi-channel support (email, SMS, push, in-app msgs), multiple notifiction types (transactional (e.g. order cofirmation)), promotional (e.g. discount offers), and system-generated alerts (e.g. password reset). Scheduled delivery for future delivery. Support rate limiting and retry mechanism. 
- 🟡 **payments**: Responsible for payment and fulfillment. Payment process is receiving purchases (made at App Store, Google, Stripe, etc) and finalizing payment. After payment, a multi-type product fulfullment (SUBSCRIPTION, CONSUMABLE, NON_CONSUMABLE) service is run and create Entitlement for particular purchases to know what User is entitled to. 
- 🟡 **posts**: Responsible for CRUD endpoints for posts and their votes.
- 🟢 **profiles**: Responsible for public-facing profile presentation data, entity hydration from object storage, and profile stats like number of followers/following, etc.
- 🟡 **registration**: Responsible for authorized user onboarding/offboarding into system safely. Registration requires submission, creation of intent token, verification email, token consumption, and then account activiated. Deregistration requires submission request, generated plain code, email sent with plain code while hashed code sits in DB, compare code input vs hash, and then soft delete User from DB. 
- 🟡 **users**: Responsible for user identity, user preferences (display preferences, feed preferences, notification preferences), and storing social graph using Fellowship/friendship models. 

## Tech Stack & Tools
* **Core Runtime:** Python 3.14 (Virtual Environment configured via `venv`)
* **Primary Framework:** Django Ninja (integrated on Django and Pydantic)
* **Storage & Cache:** Relational DB (Django ORM infrastructure) with explicit layer mappers. Plan to add caching layers. 
* **Task Queues / Async:** Pluggable queue components for notifications and media lifecycle management (TODO)
* **Object Storage:** AWS S3 integration via explicit infrastructure drivers (`shared/infrastructure/clients/s3.py`)

## Getting Started

### Prerequisites
Ensure your local system has Python 3.14+ installed globally. 

### Installation & Local Setup


1. Initialize and activate the virtual enviornment. 
   ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install Dependencies
   ```bash
    (venv) $ pip install -r requirements-dev.txt
    ```

3. Environment Configuration
- configure a local .env file or mirror values mapped out in `.env.example`
    ```bash
    cp .env.example .env
    ```
- Open .env and fill in the required values
    - DATABASE_URL - Connection string for a RDMS; I use Postgres. (default SQLite works out of the box)
    - SECRET_KEY - Generate a new Django secret key
- Can generate SECRETE_KEY using Python's secrets module
    ```bash
    python -c "from secrets import token_urlsafe; print(token_urlsafe(50))"
    ```

4. Database Migratons
   ```bash
    (venv) $ python manage.py migrate
    ```
5. Run Django Command to seed Users. Profile auto-generates with Users since Profile and User have mandatory 1-1 relationship. 
    ```bash
    (venv) $ python manage.py create_random_users --count 20
    ```
6. Run Django Command to seed Posts (script located at `apps/posts/management/commands/create_random_posts_day_by_day.py`)
    ```bash
    (venv) $ python manage.py create_random_posts_day_by_day --days 7 --min 6 --max 6 --vote-density 0.3
    ```
7. Run the Development Server
   ```bash
    (venv) $ python manage.py runserver
    ```

# Tests & CI (TODO)
* Unit tests in `tests/apps
* Unit tests for `tests/apps/*/domain/usecases/*` (mock domain interfaces)
* Integration tests for `delivery` using Django test client and test DB
* Consumer tests for Channels using `channels.testing`
* Put per-app tests under `tests/apps/<appname>/...` and integration tests under `tests/integration/`

----------------------------------------