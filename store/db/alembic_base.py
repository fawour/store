# Import all the models, so that Base class has them before being
# imported by Alembic

from .base_class import Base
from db import models
