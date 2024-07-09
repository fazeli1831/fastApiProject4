import threading
import time
from fastapi import FastAPI
from typing import Dict, Any

app = FastAPI()

class Box:
    def __init__(self):
        self.lock = threading.RLock()
        self.total_items = 0

    def execute(self, value):
        with self.lock:
            self.total_items += value

    def add(self):
        with self.lock:
            self.total_items += 1

    def remove(self):
        with self.lock:
            self.total_items -= 1

def adder(box: Box, items: int):
    print(f"N° {items} items to ADD")
    while items:
        box.add()
        time.sleep(1)
        items -= 1
        print(f"ADDED one item --> {items} items to ADD. Total items: {box.total_items}")

def remover(box: Box, items: int):
    print(f"N° {items} items to REMOVE")
    while items:
        box.remove()
        time.sleep(1)
        items -= 1
        print(f"REMOVED one item --> {items} items to REMOVE. Total items: {box.total_items}")

@app.get("/process-items/{add_items}/{remove_items}", response_model=Dict[str, Any])
def process_items(add_items: int, remove_items: int):
    box = Box()

    t1 = threading.Thread(target=adder, args=(box, add_items))
    t2 = threading.Thread(target=remover, args=(box, remove_items))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    return {"total_items": box.total_items}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
