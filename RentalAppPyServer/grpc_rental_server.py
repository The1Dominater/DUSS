#!/usr/bin/env python3
import grpc
import rental_app_pb2_grpc
import rental_app_pb2
from concurrent import futures

from datetime import datetime

TAX = 0.08

class ageServicer(rental_app_pb2_grpc.ageServicer):
    def age(self,request,context):
        # Make an imageReply obj
        response = rental_app_pb2.ageReply()
        response.age = 21

        try:
            birthday = request.birthday,
            if isinstance(birthday,(int)):
                birthday = str(birthday)
            if len(birthday) < 8:
                birthday = '0' + birthday
            
            birth_date = datetime.strptime(request.birthday, "%m/%d/%Y")
            today = datetime.today()
            # Calculate the difference in years
            age = today.year - birth_date.year
            # Adjust if the birthday hasn't occurred yet this year
            if (today.month, today.day) < (birth_date.month, birth_date.day):
                age -= 1
            response.age = age
        except Exception:
            print("Error could not calculate age")

        print("Handled age request")
        return response

class dinServicer(rental_app_pb2_grpc.dinServicer):
    def din(self,request,context):
        response = rental_app_pb2.dinReply()

        age = request.age
        height = request.height
        h_unit = request.h_unit
        weight = request.weight
        w_unit = request.w_unit
        skier_type = request.skier_type
        boot_size = 235 #TODO I forgot to include this when generating protos

        try:
            height = request.height
            h_unit = request.h_unit
            weight = request.weight
            w_unit = request.w_unit
            skier_type = request.skier_type

            # Convert in to cm
            if h_unit == 2:
                height = height * 2.54
            # Conver lbs to kgs
            if w_unit == 2:
                weight = weight * 0.454
            
            # Calculate base DIN based on height and weight (simplified approximation)
            base_din = round((weight / 10) + (height / 100), 1)
            
            # Adjust DIN based on skier type
            if skier_type == 1:
                base_din *= 0.75
            elif skier_type == 3:
                base_din *= 1.25 
            
            # Adjust DIN based on age (older skiers tend to have lower DIN)
            if age > 50:
                base_din -= 1
            
            # Adjust based on boot size (larger boot sizes require higher DIN)
            if boot_size >= 28:
                base_din += 1
            
            # Ensure DIN is within standard range (usually between 3 and 12)
            base_din = max(3, min(base_din, 12))

            response.din = base_din
        except:
            print("Error")
        
        print("Handled din request")
        return response

class totalServicer(rental_app_pb2_grpc.totalServicer):
    def total(self,request,context):
        response = rental_app_pb2.totalReply()
        try:
            eq_type = request.eq_type
            lease_type = request.lease_type
            pkg_type = request.pkg_type

            if eq_type == 'ski' and lease_type == 1:
                if pkg_type == 1:
                    total_cost = 350
                elif pkg_type == 2:
                    total_cost = 250
                elif pkg_type == 3:
                    total_cost = 150
                else:
                    total_cost = 100
            elif eq_type == 'snowboard' and lease_type == 1:
                if pkg_type == 1:
                    total_cost = 375
                elif pkg_type == 2:
                    total_cost = 235    
                elif pkg_type == 3:
                    total_cost = 150
                else:
                    total_cost = 100
            else:
                if pkg_type == 1:
                    total_cost = 80
                elif pkg_type == 2:
                    total_cost = 70    
                elif pkg_type == 3:
                    total_cost = 50
                else:
                    total_cost = 35
            
            final_cost = total_cost * TAX
            response.total = final_cost
        except:
            print("Error in cost calculation")
        
        print("Handled total request")
        return response

# Setup grpc server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

rental_app_pb2_grpc.add_ageServicer_to_server(ageServicer(),server)
rental_app_pb2_grpc.add_dinServicer_to_server(dinServicer(),server)
rental_app_pb2_grpc.add_totalServicer_to_server(totalServicer(),server)

port = 50051
print(f"Starting server. Listening on port {port}")
server.add_insecure_port("[::]:50051")
server.start()
server.wait_for_termination()