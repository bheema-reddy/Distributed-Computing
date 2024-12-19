import grpc
import delivery_pb2
import delivery_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = delivery_pb2_grpc.DeliveryServiceStub(channel)

        # Example location updates with different statuses
        statuses = ["Pending", "Pre-Transit", "In Transit", "Out for Delivery", "Failed Attempt", "Delivered"]
        for status in statuses:
            response = stub.SendLocationUpdate(
                delivery_pb2.LocationRequest(
                    vehicle_id="V123",
                    latitude=35.6895,
                    longitude=139.6917,
                    status=status
                )
            )
            print(response.message)

if __name__ == '__main__':
    run()
