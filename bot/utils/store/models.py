from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    first_name: str
    chat_id: int
    
    def to_database(self) -> None:
        self.username = self.username.lower()
        self.first_name = self.first_name.lower()
        return 
    
    def to_message(self) -> None:
        self.first_name = self.first_name.capitalize()
        return 
