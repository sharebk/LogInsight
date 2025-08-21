import random
import uuid
from datetime import datetime, timedelta
import multiprocessing

services = ["auth-service", "payment-service", "inventory-service", "order-service", "notification-service"]
methods = ["GET", "POST", "PUT", "DELETE"]
paths = ["/api/v1/users", "/api/v1/orders", "/api/v1/products", "/api/v1/payments"]

class LogGenerator:
    def __init__(self):
        self.base_time = datetime.now()
        
    def generate_log(self, _):
        log_time = self.base_time - timedelta(seconds=random.randint(0, 86400))
        level = random.choices(["INFO", "WARNING", "ERROR"], weights=[0.7, 0.2, 0.1])[0]
        
        log = {
            "timestamp": log_time.isoformat(),
            "level": level,
            "service": random.choice(services),
            "request_id": str(uuid.uuid4()),
            "client_ip": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "method": random.choice(methods),
            "path": random.choice(paths),
            "status_code": random.choice([200, 201, 400, 401, 403, 404, 500]),
            "response_time": random.randint(10, 5000)
        }
        
        if level == "ERROR":
            errors = ["Database connection failed", "Invalid request payload", "Service timeout", "Authentication failed"]
            log["error"] = random.choice(errors)
            
        return f"{log['timestamp']} {log['level']} {log['service']} {log['request_id']} {log['client_ip']} {log['method']} {log['path']} {log['status_code']} {log['response_time']}ms" + (f" error=\"{log['error']}\"" if level == "ERROR" else "") + "\n"

def generate_logs():
    generator = LogGenerator()
    with open("rfc_logs.log", "w") as f:
        with multiprocessing.Pool() as pool:
            for log in pool.imap(generator.generate_log, range(10000)):
                f.write(log)

if __name__ == "__main__":
    generate_logs()