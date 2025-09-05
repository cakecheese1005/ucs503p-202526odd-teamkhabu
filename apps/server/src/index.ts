import express from 'express'
import dotenv from 'dotenv'
import cors from 'cors'
import helmet from 'helmet'
import morgan from 'morgan'

dotenv.config()

const app = express()

app.use(helmet())
app.use(morgan('dev'))

// 🔐 Middleware
app.use(cors())
app.use(express.json())

app.get('/', (req, res) => res.send('Backend is running!'))

const PORT = process.env.PORT || 3000
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`)
})
