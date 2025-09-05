import express from 'express'
import dotenv from 'dotenv'
import cors from 'cors'
import helmet from 'helmet'
import morgan from 'morgan'
import { data } from './utils/data'

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

app.post('/search', (req, res) => {
  const { start, end } = req.body

  if (!start || !end) {
    return res.status(400).json({ error: 'start and end are required' })
  }

  //@ts-ignore
  const results = data.filter((trip) => {
    return (
      trip.start.toLowerCase() === start.toLowerCase() &&
      trip.destination.toLowerCase() === end.toLowerCase()
    )
  })

  res.json({ results })
})

const PORT = process.env.PORT || 3001
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`)
})
