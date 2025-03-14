from faker import Faker

fake = Faker()

class Payloads:

    def valid_post():
        return {
            "userId": fake.random_int(),
            "id": fake.random_int(),
            "title": fake.sentence(),
            "body": fake.text()
        }
    
    def body_only():
        return {
            "body": fake.text()
        }
    
    def without_title():
        return {
            "userId": fake.random_int(),
            "id": fake.random_int(),
            "body": fake.text()            
        }

    def without_id():
        return {
            "userId": fake.random_int(),
            "title": fake.sentence(),
            "body": fake.text()            
        }
    
    def without_userId():
        return {
            "id": fake.random_int(),
            "title": fake.sentence(),
            "body": fake.text()            
        }

    def without_body():
        return {
            "userId": fake.random_int(),
            "id": fake.random_int(),
            "title": fake.sentence(),         
        }

    def empty():
        return {

        }
    
    def valid_put():
        return {
            "body": "changed_text"
        }