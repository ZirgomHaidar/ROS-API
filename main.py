import uvicorn
from ROSAPI import app

def main():
    uvicorn.run(app, log_config=None)

if __name__ == "__main__":
    main()
