import grpc
from concurrent import futures
import delivery_pb2
import delivery_pb2_grpc
from kafka import KafkaProducer
import json

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class DeliveryService(delivery_pb2_grpc.DeliveryServiceServicer):
    def SendLocationUpdate(self, request, context):
        data = {
            'vehicle_id': request.vehicle_id,
            'latitude': request.latitude,
            'longitude': request.longitude,
            'status': request.status  # Include status in the message
        }
        producer.send('location_updates', value=data)
        producer.flush()
        return delivery_pb2.LocationResponse(message=f"Location update received with status: {request.status}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    delivery_pb2_grpc.add_DeliveryServiceServicer_to_server(DeliveryService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
