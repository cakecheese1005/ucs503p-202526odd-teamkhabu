import express from 'express'
import dotenv from 'dotenv'
import cors from 'cors'
import helmet from 'helmet'
import morgan from 'morgan'

dotenv.config()

const app = express()

app.use(helmet())
app.use(morgan('dev'))
app.use(cors())
app.use(express.json())

// 🚗 In-memory trips storage (dummy)
interface Trip {
  id: string
  creatorId: string
  start: string
  destination: string
  date: string
  groupSize: number
  members: string[]
  isGirlsOnly: boolean
  status: 'OPEN' | 'FULL' | 'CANCELLED'
}

let trips: Trip[] = []

// ✅ Health check
app.get('/', (req, res) => res.send('Backend is running!'))

// ➕ Create trip
app.post('/trips', (req, res) => {
  const { creatorId, start, destination, date, groupSize, isGirlsOnly } = req.body
  const newTrip: Trip = {
    id: `trip_${trips.length + 1}`,
    creatorId,
    start,
    destination,
    date,
    groupSize,
    members: [creatorId],
    isGirlsOnly,
    status: 'OPEN'
  }
  trips.push(newTrip)
  res.status(201).json(newTrip)
})

// 📜 List trips
app.get('/trips', (req, res) => {
  res.json(trips)
})

// 👥 Join trip
app.post('/trips/:id/join', (req, res) => {
  const { userId } = req.body
  const trip = trips.find(t => t.id === req.params.id)

  if (!trip) return res.status(404).json({ message: 'Trip not found' })
  if (trip.status !== 'OPEN') return res.status(400).json({ message: 'Trip not open for joining' })
  if (trip.members.includes(userId)) return res.status(400).json({ message: 'Already joined' })

  if (trip.members.length < trip.groupSize) {
    trip.members.push(userId)
    if (trip.members.length === trip.groupSize) trip.status = 'FULL'
    return res.json(trip)
  }

  res.status(400).json({ message: 'Group is full' })
})

// 👋 Leave trip
app.post('/trips/:id/leave', (req, res) => {
  const { userId } = req.body
  const trip = trips.find(t => t.id === req.params.id)

  if (!trip) return res.status(404).json({ message: 'Trip not found' })
  if (!trip.members.includes(userId)) return res.status(400).json({ message: 'User not part of this trip' })

  trip.members = trip.members.filter(id => id !== userId)
  if (trip.status === 'FULL' && trip.members.length < trip.groupSize) {
    trip.status = 'OPEN'
  }

  res.json(trip)
})

const PORT = process.env.PORT || 3000
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`)
})
