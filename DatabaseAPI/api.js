const express = require("express");
var app = express.Router();
const bodyParser = require('body-parser');
const helmet = require('helmet');
const cors = require('cors');
const db_queries = require('./db.js');
const db = new db_queries();

// Apply middleware
// Helmet for security
app.use(helmet());

// CORS for cross-origin allowance
app.use(cors());

// Body-parser for parsing JSON and urlencoded data
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.json({status: true, message: "API is operative"});
})

app.get('/user/:bluetoothCode', async (req, res) => {
  const bluetoothCode = req.params.bluetoothCode;
  if (!bluetoothCode) return res.json({status: false, message: "No bluetoothCode provided"});
  if (bluetoothCode.length < 1) return res.json({status: false, message: "Invalid bluetoothCode"});
  const user = await db.get_user(bluetoothCode);
  res.json(user);
});

app.post('/users', async (req,res) => {
  const usersDelimited = req.body.codes;
  if (!usersDelimited || usersDelimited.length < 1)
    return res.json({status: false, message: "No users provided"});
  const users = usersDelimited.split(',');
  const user = await db.get_users(users);
  if (user.status === false) return res.json({status: user.status, message: user.message, data: {}});
  res.json(user);
})

app.get('/ads', async (req, res) => {
  const ads = await db.get_ads();
  res.json(ads);
});

app.post('/putAdvertiser', async (req, res) => {
  const name = req.body.name;
  const budget = req.body.budget;
  if (!name || !budget) return res.json({status: false, message: "Missing parameters"});
  if (name.length < 1 || budget < 0) return res.json({status: false, message: "Invalid parameters"});
  const advertiser = await db.put_advertiser(name, budget);
  res.json(advertiser);
});

app.post('/putAd', async (req, res) => {
  const [adType, health_preferences, food_preferences, clothing_preferences, electronics_preferences, entertainment_preferences, beauty_preferences, home_preferences, automative_preferences, other_preferences, url, name, budget, bid] = [req.body.adType || 0, req.body.health_preferences, req.body.food_preferences, req.body.clothing_preferences, req.body.electronics_preferences, req.body.entertainment_preferences, req.body.beauty_preferences, req.body.home_preferences, req.body.automative_preferences, req.body.other_preferences, req.body.url, req.body.name, req.body.budget, req.body.bid];
  console.log(req.body)
  if (
    adType === undefined || adType === null || 
    health_preferences === undefined || health_preferences === null || 
    food_preferences === undefined || food_preferences === null || 
    clothing_preferences === undefined || clothing_preferences === null || 
    electronics_preferences === undefined || electronics_preferences === null || 
    entertainment_preferences === undefined || entertainment_preferences === null || 
    beauty_preferences === undefined || beauty_preferences === null || 
    home_preferences === undefined || home_preferences === null || 
    automative_preferences === undefined || automative_preferences === null || 
    other_preferences === undefined || other_preferences === null || 
    url === undefined || url === null || 
    name === undefined || name === null || 
    budget === undefined || budget === null || 
    bid === undefined || bid === null
  ) {
    return res.json({status: false, message: "Missing parameters"});
  }
  if (url.length < 1 || name.length < 1 || budget < 0 || bid < 0)
    return res.json({status: false, message: "Invalid URL"});
  const advertiser = await db.put_advertiser(name, budget);
  if (advertiser.status === false) return res.json(advertiser);
  const advertiserID = advertiser.rows.insertId;
  const ad = await db.put_ad(adType, health_preferences, food_preferences, clothing_preferences, electronics_preferences, entertainment_preferences, beauty_preferences, home_preferences, automative_preferences, other_preferences, url, advertiserID, bid);
  res.json(ad);
});

app.get('*', (req, res) => {
  res.status(404).json({status: false, message: "Invalid endpoint"});
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

module.exports = app;