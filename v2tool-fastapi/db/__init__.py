from .client import engine
from .models import *

Base.metadata.create_all(bind=engine)
