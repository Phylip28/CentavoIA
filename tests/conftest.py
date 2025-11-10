from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.adapters.persistence.database import Base
from app.core.config import settings

# Use the SAME database URL that docker-compose reads
# Note: This test MUST run INSIDE the dev container
engine = create_engine(str(settings.DATABASE_URL))

# Create a session factory ONLY FOR TESTS
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Pytest fixture that provides a clean database session for each test.

    This fixture:
    1. Creates all tables before the test
    2. Provides a fresh session to the test
    3. Rolls back any changes after the test
    4. Drops all tables for complete cleanup
    """
    # 1. Create tables (idempotent operation)
    Base.metadata.create_all(bind=engine)

    # 2. Start a new session
    session = TestSessionLocal()

    try:
        # 3. Provide the session to the test (with 'yield')
        yield session
    finally:
        # 4. After the test, cleanup and close
        session.rollback()  # Undo any changes
        session.close()

    # 5. Drop all tables (for complete cleanup)
    Base.metadata.drop_all(bind=engine)
