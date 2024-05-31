from app import app
from flask import Flask
from app.controllers.sensor_controller import receive_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
