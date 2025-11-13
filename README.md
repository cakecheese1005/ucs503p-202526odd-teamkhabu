🚗 Overview

RideShare is a full-stack ride-sharing platform built for Thapar University students.
It allows students to:

Create rides (groups)

Join rides

Search rides with mutual connections

Connect with other users (friend system)

Manage profile, connections, created/joined rides

Use Expo React Native App (Android + iOS + Web)

Backend powered by Node.js + Express + PostgreSQL

Optional ML/Recommender micro-service using Python + Flask


PROJECT STRUCTURE 
/
├── backend/
│   ├── server.js
│   ├── schema.sql
│   ├── algo.py
│   ├── algo_service.py
│   └── python_city.py
│
├── mobile/   (React Native + Expo cross-platform app)
│   ├── App.js
│   ├── app.config.js
│   ├── screens/
│   │   ├── LoginScreen.js
│   │   ├── GroupsScreen.js
│   │   ├── CreateTripScreen.js
│   │   ├── GroupDetailsScreen.js
│   │   └── ProfileScreen.js
│   ├── components/
│   │   ├── MapBackdrop.native.js
│   │   └── MapBackdrop.web.js
│   └── vercel.json


TECHSTACK

Backend

Node.js + Express

PostgreSQL

JWT Authentication

GeoNames City Dataset Loader

Render Deployment Support

Optional ML micro-service (Flask)

Frontend (Mobile/Web)

React Native (Expo)


Key Features
🧭 Ride Creation

Start & destination city

Intermediate stops

Female-only groups

Capacity

Departure time picker

Validation: One of start/dest must be Patiala

🕵️ Ride Search

Search by route

Filter by preference

Filter by mutual connections

Time window search

Ranking by mutual connections + availability

👥 Social Features

Connect with other riders

Auto-hide Connect button when already connected

Connections tab in profile

🔐 Authentication

Thapar email only (@thapar.edu)

JWT access + refresh token system

📍 Map Backdrop

Mobile → React Native Maps

Web → OpenStreetMap embed

Navigation (Stack + Bottom Tabs)

AsyncStorage (JWT storage)

Map Backdrops (React Native Maps + OSM iframe)

Expo Web Deploy via Vercel
