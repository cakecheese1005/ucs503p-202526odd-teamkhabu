DEPLOYED LINK:https://ucs503p-202526odd-teamkhabu.vercel.app/


Youtube VIDEO:https://youtu.be/YH25fHVGqjI?si=1Jd4xIxkQYKInCy5

QR :
<img width="400" height="500" alt="image" src="https://github.com/user-attachments/assets/bd2cb15e-5230-4919-85a8-38b2f75877aa" />


Overview
🚗
RideShare is a full-stack ride-sharing platform for Thapar University.
A Smart Carpooling & Group Ride System that enables students and commuters to find, create, and join ride groups safely and efficiently.


Features:

• Create rides

• Join rides

• Search rides with mutual connections

• Social connect system

• Profile + Ride history

• Mobile + Web app

• Node.js + PostgreSQL backend

• Optional Python recommender service


Project Structure

<img width="400" height="500" alt="image" src="https://github.com/user-attachments/assets/895f0ea4-d1b4-400c-ad1e-d94e5f6e55b4" />



Tech Stack

Backend:
Node.js, Express, PostgreSQL, JWT, Render

Frontend:
React Native (Expo), OSM Maps, Vercel

✨ Key Features

🧭 Ride Creation

Start & destination city

Intermediate stops

Female-only groups

Capacity selection

Departure time picker

Important validation: One of start or dest must be Patiala

🕵️ Ride Search

Search by route

Filter by preference (ALL / FEMALE_ONLY)

Filter by mutual connections

Time-window search

Sorting based on:

mutual connection strength
seats available

👥 Social Features

Connect with other riders

Auto-hide Connect button for existing connections

Connections tab inside Profile screen


🔐 Authentication

Thapar email only → @thapar.edu

JWT access + refresh token system

Secure token storage using AsyncStorage


🗺 Map Backdrop

Mobile: React Native Maps (animated camera + blur layer)

Web: OpenStreetMap embedded view
