from fastapi import FastAPI
from app.db.database import Base, engine
from app.routes import user, restaurant, order, payment, auth
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CollectorRegistry
from fastapi.responses import Response
from datetime import datetime,timedelta
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI()
# Prometheus Metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds', ['method','endpoint'])
ACTIVE_USERS = Gauge('active_users', 'Number of active users')

# Instrumentator setup
Instrumentator().instrument(app).expose(app)

# Metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

# Middleware to track metrics
@app.middleware("http")
async def add_request_metrics(request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    latency = (datetime.now() - start_time).total_seconds()
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(latency)
    return response

Base.metadata.create_all(bind=engine)
app.include_router(user.router, prefix="/users")

app.include_router(user.router)
app.include_router(restaurant.router)
app.include_router(order.router)
app.include_router(payment.router)
app.include_router(auth.router)