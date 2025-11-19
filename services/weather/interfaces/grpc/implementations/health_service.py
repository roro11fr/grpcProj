from services.weather.interfaces.grpc.generated import health_pb2, health_pb2_grpc


class HealthServiceImpl(health_pb2_grpc.HealthServiceServicer):
    def HealthCheck(self, request, context):
        print(f"Received request: {request}")
        return health_pb2.HealthCheckResponse(status="SERVING")
