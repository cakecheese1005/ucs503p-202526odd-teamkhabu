# 🚗 College Car Pooling App

A secure and interactive car/taxi pooling platform designed specifically for college students. Connect with fellow students to share rides, reduce travel costs, and build a sustainable campus community.

## 🌟 Features

### Core Functionality
- **College-Only Access**: Secure authentication using college email IDs
- **Smart Trip Search**: Find rides based on destination, date, and available seats
- **Real-time Chat**: Private messaging with trip creators and group chats for accepted participants
- **Request-Based System**: Join requests with email notifications for trip creators
- **Gender-Specific Trips**: Optional girls-only trips for enhanced safety
- **Profile Management**: Year, branch, and gender-based filtering

### Safety & Security
- **Verified Users**: College ID verification ensures trusted community
- **Gender-Based Filtering**: Girls-only trip options with backend enforcement
- **Request Approval**: Trip creators manually approve join requests
- **Email Notifications**: Automated alerts for all trip activities

## 🛠️ Tech Stack

### Frontend
- **React.js** - Modern UI components
- **Tailwind CSS** - Responsive styling
- **Socket.io Client** - Real-time chat functionality

### Backend
- **Node.js + Express** - RESTful API server
- **Prisma ORM** - Type-safe database operations
- **JWT Authentication** - Secure session management
- **Socket.io** - WebSocket connections for chat
- **Nodemailer** - Email notification service

### Database
- **PostgreSQL** - Primary database
- **Prisma Client** - Database queries and migrations

### Deployment
- **Frontend**: Vercel/Netlify
- **Backend**: Render/Railway
- **Database**: Railway PostgreSQL/Supabase

## 📊 Database Schema

### Entity Relationship Diagram

```mermaid
erDiagram
    User ||--o{ Trip : creates
    User ||--o{ JoinRequest : makes
    User ||--o{ TripParticipant : participates
    User ||--o{ Message : sends
    User ||--o{ Notification : receives
    
    Trip ||--o{ JoinRequest : receives
    Trip ||--o{ TripParticipant : has
    Trip ||--o{ Message : contains
    Trip ||--o{ Notification : triggers
    
    User {
        string id PK
        string collegeId UK
        string name
        string year
        string branch
        string gender
        string passwordHash
        boolean verified
        datetime createdAt
        datetime updatedAt
    }
    
    Trip {
        string id PK
        string creatorId FK
        string start
        string destination
        datetime date
        int seatsAvailable
        boolean isGirlsOnly
        enum status
        datetime createdAt
        datetime updatedAt
    }
    
    JoinRequest {
        string id PK
        string requesterId FK
        string tripId FK
        enum status
        datetime createdAt
    }
    
    TripParticipant {
        string id PK
        string userId FK
        string tripId FK
        datetime joinedAt
    }
    
    Message {
        string id PK
        string content
        string senderId FK
        string tripId FK
        string receiverId FK
        datetime createdAt
    }
    
    Notification {
        string id PK
        string userId FK
        string message
        string tripId FK
        boolean read
        datetime createdAt
    }
```

### Key Relationships
- **User → Trip**: One-to-many (creator relationship)
- **Trip → TripParticipant**: One-to-many (participants)
- **User → JoinRequest**: One-to-many (user requests)
- **Trip → JoinRequest**: One-to-many (trip requests)
- **Message**: Supports both private (user-to-user) and group (trip-wide) chat

## 🚀 Getting Started

### Prerequisites
- Node.js (v16+)
- PostgreSQL database
- College email account for registration

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/college-car-pooling.git
cd college-car-pooling
```

2. **Install dependencies**
```bash
# Backend
cd backend
npm install

# Frontend
cd ../frontend
npm install
```

3. **Environment Setup**
```bash
# Backend .env
DATABASE_URL="postgresql://username:password@localhost:5432/pooling_db"
JWT_SECRET="your-jwt-secret"
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="your-email@gmail.com"
SMTP_PASS="your-app-password"

# Frontend .env
REACT_APP_API_URL="http://localhost:3001"
REACT_APP_SOCKET_URL="http://localhost:3001"
```

4. **Database Setup**
```bash
cd backend
npx prisma migrate dev --name init
npx prisma generate
```

5. **Start Development Servers**
```bash
# Backend (Port 3001)
cd backend
npm run dev

# Frontend (Port 3000)
cd frontend
npm start
```

## 📱 API Documentation

### Authentication
```http
POST /auth/register
POST /auth/login
```

### Trip Management
```http
GET    /trips              # Search trips
POST   /trips              # Create trip
POST   /trips/:id/request  # Request to join
```

### Request Management
```http
GET    /trips/:id/requests # View trip requests
POST   /requests/:id/accept # Accept request
POST   /requests/:id/reject # Reject request
```

### Chat System
```http
GET    /chat/:tripId       # Get chat history
POST   /chat/:tripId/message # Send message
```

### WebSocket Events
```javascript
// Join trip chat room
socket.emit('join-trip', tripId)

// Send message
socket.emit('send-message', { tripId, content, receiverId })

// Receive messages
socket.on('new-message', messageData)
```

## 🔒 Security Features

- **College Email Verification**: Only verified college students can access
- **JWT Token Authentication**: Secure session management
- **Gender-Based Access Control**: Backend enforcement of girls-only trips
- **Request Approval System**: Manual approval prevents unauthorized joins
- **Input Validation**: Comprehensive data sanitization
- **Rate Limiting**: Prevents spam and abuse

## 🎯 User Flow

1. **Registration**: Students register with college email ID
2. **Profile Setup**: Add year, branch, gender information
3. **Trip Creation**: Create trips with destination, date, seats
4. **Trip Search**: Find relevant trips using filters
5. **Join Request**: Send request with private chat capability
6. **Approval Process**: Creator reviews and approves/rejects
7. **Group Coordination**: Approved members join group chat
8. **Trip Completion**: Mark trips as completed

## 🚧 Future Enhancements

- **Payment Integration**: Razorpay for bill splitting
- **Rating System**: User ratings for safety and reliability
- **AI Recommendations**: Smart trip suggestions based on history
- **Geolocation**: GPS-based pickup point suggestions
- **Mobile App**: React Native mobile application
- **Admin Dashboard**: College administration oversight panel

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- Built for college students, by college students
- Inspired by the need for safe and affordable transportation
- Thanks to the open-source community for amazing tools

---

⭐ **Star this repo if you find it helpful!** ⭐
