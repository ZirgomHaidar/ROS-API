# RisingOS API [v1.0.0]

A RESTful API made using **FASTAPI written in Python(v3.11 and above)** service that provides OTA (Over-The-Air) update information for RisingOS ROM. This API fetches and serves data from the [RisingOTA](https://github.com/RisingOSS-devices/android_vendor_RisingOTA) repository, making it easy to access device-specific ROM information programmatically.

### TODO List

- [x] Endpoints rename to API naming convention
- [x] Project Restructure with separate concerns (routes, services, models)

### Features

- RESTful endpoints for accessing ROM information
- Real-time data synchronization with RisingOTA repository
- Cached responses for improved performance
- Comprehensive device and build information
- JSON response format

### Prerequisites

- fastapi[standard]>=0.112.0
- requests
- pydantic
- apscheduler
- git

### API Documentation

you can access:

- Swagger UI documentation at https://ros-api-2to4.onrender.com/docs
- ReDoc documentation at https://ros-api-2to4.onrender.com/redoc

### API Endpoints

1. API status
```
GET /
```

2. DeviceList
```
GET /api/v1/device/deviceList
```

3. Device Variants and Information
```
GET /api/v1/device/{codename}
```
**example**: /device/_lynx_, /device/_cancunf_, etc.

### Project Structure
```
├── main.py
└── ROSAPI
│   ├── functions
│   │   ├── DeviceList.py
│   │   └── DeviceVaraints.py
│   ├── __init__.py
│   └── Models
│       ├── DnListModel.py
│       └── __init__.py
│
├── README.md
├── requirements.txt
```
