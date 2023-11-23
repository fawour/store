import functools
from contextvars import ContextVar, Token
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from core.config import settings

session_context: ContextVar[str] = ContextVar("session_context")

engine = create_engine(settings.DATABASE_URL, pool_recycle=300, pool_pre_ping=True, pool_use_lifo=True)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


session: Session = scoped_session(session_factory=SessionFactory, scopefunc=get_session_context)


def standalone_session(func):
    """
    According to the current settings, the session is set through middleware.
    However, it doesn't go through middleware in tests or background tasks.
    So you need to use the `@standalone_session` decorator.

    @standalone_session
    def test_something():
        ...
    """
    @functools.wraps(func)
    def _standalone_session(*args, **kwargs):
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            return func(*args, **kwargs)
        finally:
            session.close()
            reset_session_context(context=context)

    return _standalone_session


def autocommit(func):
    @functools.wraps(func)
    def _autocommit(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            session.commit()
            return result
        except Exception:
            session.rollback()
            raise

    return _autocommit
