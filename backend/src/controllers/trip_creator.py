from typing import Dict
from src.drivers.email_sender import send_email
import uuid

class TripCreator:
    def __init__(self, trip_repository, emails_repository, participants_repository) -> None:
        self.__trip_repository = trip_repository
        self.__emails_repository = emails_repository
        self.__participants_repository = participants_repository
    
    def create(self, body) -> Dict:
        try:
            emails = body.get("emails_to_invite", [])

            trip_id = str(uuid.uuid4())
            trip_infos = {
                "id": trip_id,
                "destination": body["destination"],
                "start_date": body["start_date"],  # Corrigido para o nome correto
                "end_date": body["end_date"],      # Corrigido para o nome correto
                "owner_name": body["owner_name"],
                "owner_email": body["owner_email"]
            }
            print("Trip info:", trip_infos)  # Log para depuração

            self.__trip_repository.create_trip(trip_infos)

            for email in emails:
                email_data = {
                    "email": email,
                    "trip_id": trip_id,
                    "id": str(uuid.uuid4())
                }
                self.__emails_repository.registry_email(email_data)
                print("Registered email:", email_data)  # Log para depuração

                # Criação do participante associado ao email
                participant_data = {
                    "id": email_data["id"],  # Mesmo ID usado para o email
                    "trip_id": trip_id,
                    "emails_to_invite_id": email_data["id"],  # Mesmo ID usado para o email
                    "name": ""  # Nome do participante, se disponível
                }
                self.__participants_repository.registry_participant(participant_data)
                print("Registered participant:", participant_data)  # Log para depuração

            send_email(
                [body["owner_email"]],
                f"http://localhost:3000/trips/{trip_id}/confirm"
            )
            
            return {
                "body": {"id": trip_id},
                "status_code": 201
            }
        except Exception as exception:
            print("Exception:", str(exception))  # Log para depuração
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }
