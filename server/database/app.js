const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const path = require('path');

const app = express();
const port = process.env.PORT || 3030;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// Resolve JSON paths
const reviewsPath = fs.existsSync(path.join(__dirname, 'reviews.json'))
  ? path.join(__dirname, 'reviews.json')
  : path.join(__dirname, 'data', 'reviews.json');

const dealershipsPath = fs.existsSync(path.join(__dirname, 'dealerships.json'))
  ? path.join(__dirname, 'dealerships.json')
  : path.join(__dirname, 'data', 'dealerships.json');

let reviews_data = JSON.parse(fs.readFileSync(reviewsPath, 'utf8'));
let dealerships_data = JSON.parse(fs.readFileSync(dealershipsPath, 'utf8'));

let inMemoryReviews = [...reviews_data.reviews];
let inMemoryDealerships = [...dealerships_data.dealerships];

const mongoUrl = process.env.MONGO_URL || "mongodb://mongo_db:27017/";
let useMongo = false;

const Reviews = require('./review');
const Dealerships = require('./dealership');

mongoose.connect(mongoUrl, { dbName: 'dealershipsDB', serverSelectionTimeoutMS: 2000 })
  .then(async () => {
    useMongo = true;
    console.log("Connected to MongoDB successfully");
    try {
      await Reviews.deleteMany({});
      await Reviews.insertMany(inMemoryReviews);
      await Dealerships.deleteMany({});
      await Dealerships.insertMany(inMemoryDealerships);
      console.log("MongoDB collections populated");
    } catch (e) {
      console.error("Error populating MongoDB:", e);
    }
  })
  .catch((err) => {
    console.warn("MongoDB connection failed, falling back to in-memory/JSON store:", err.message);
    useMongo = false;
  });

// Express route to home
app.get('/', async (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    if (useMongo) {
      const documents = await Reviews.find();
      return res.json(documents);
    }
    return res.json(inMemoryReviews);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id, 10);
    if (useMongo) {
      const documents = await Reviews.find({ dealership: dealerId });
      return res.json(documents);
    }
    const matching = inMemoryReviews.filter(r => parseInt(r.dealership, 10) === dealerId);
    return res.json(matching);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    if (useMongo) {
      const dealerships = await Dealerships.find();
      return res.status(200).json(dealerships);
    }
    return res.status(200).json(inMemoryDealerships);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// Express route to fetch dealerships by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  const state = req.params.state;
  try {
    if (useMongo) {
      const dealerships = await Dealerships.find({
        state: { $regex: new RegExp(`^${state}$`, 'i') }
      });
      if (!dealerships || dealerships.length === 0) {
        return res.status(404).json({ error: `No dealerships found in state: ${state}` });
      }
      return res.json(dealerships);
    }
    const filtered = inMemoryDealerships.filter(
      d => d.state && d.state.toLowerCase() === state.toLowerCase()
    );
    if (filtered.length === 0) {
      return res.status(404).json({ error: `No dealerships found in state: ${state}` });
    }
    return res.json(filtered);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

// Express route to fetch dealers by ID
app.get('/fetchDealer/:id', async (req, res) => {
  const id = parseInt(req.params.id, 10);
  try {
    if (useMongo) {
      const dealership = await Dealerships.findOne({ id });
      if (!dealership) {
        return res.status(404).json({ error: `No dealership found with ID: ${id}` });
      }
      return res.json(dealership);
    }
    const found = inMemoryDealerships.find(d => parseInt(d.id, 10) === id);
    if (!found) {
      return res.status(404).json({ error: `No dealership found with ID: ${id}` });
    }
    return res.json(found);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealership by ID' });
  }
});

// Express route to insert review
app.post('/insert_review', async (req, res) => {
  let data = req.body;
  if (typeof data === 'string' || Buffer.isBuffer(data)) {
    try {
      data = JSON.parse(data.toString());
    } catch (e) {
      // already parsed or unparseable
    }
  }

  try {
    let new_id = 1;
    if (useMongo) {
      const documents = await Reviews.find().sort({ id: -1 }).limit(1);
      if (documents && documents.length > 0 && documents[0].id) {
        new_id = documents[0].id + 1;
      }
    } else if (inMemoryReviews.length > 0) {
      const maxId = Math.max(...inMemoryReviews.map(r => r.id || 0));
      new_id = maxId + 1;
    }

    const reviewObj = {
      id: new_id,
      name: data.name,
      dealership: parseInt(data.dealership, 10),
      review: data.review,
      purchase: Boolean(data.purchase),
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: parseInt(data.car_year, 10) || data.car_year
    };

    if (useMongo) {
      const reviewDoc = new Reviews(reviewObj);
      const savedReview = await reviewDoc.save();
      return res.json(savedReview);
    }

    inMemoryReviews.push(reviewObj);
    return res.json(reviewObj);
  } catch (error) {
    console.error("Error inserting review:", error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
