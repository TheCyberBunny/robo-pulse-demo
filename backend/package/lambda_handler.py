"""
RoboPulse Fleet Command Center
Day 9 - the entrypoint AWS Lambda actually calls. Mangum translates
between Lambda's event/context invocation model and the ASGI
interface FastAPI already speaks - app.main:app itself needs zero
changes to run inside Lambda.
"""

from mangum import Mangum

from app.main import app

handler = Mangum(app)