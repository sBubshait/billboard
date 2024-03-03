const mysql = require('mysql2/promise')
var con = mysql.createPool({
  host: "YOUR_MOM",
 user: "root",
 password: "don't_look_here_idiot",
 database: "home"
});

module.exports = class db {
  constructor() {
    
  }

  async get_user(bluetoothCode) {
    console.log("REQUESTING")
    const query = "SELECT * FROM users WHERE bluetoothCode = ?"
    const [rows] = await con.query(query, [bluetoothCode])
    if (!rows[0]) return {status: false, message: "User not found"}
    return {status: true, user: rows[0]}
  }

  async get_users(users) {
    const query = `
      SELECT 
        CASE WHEN COUNT(*) = 0 THEN false
        ELSE true END AS has_users,
        AVG(health_preferences) AS health,
        AVG(food_preferences) AS food,
        AVG(clothing_preferences) AS clothing,
        AVG(entertainment_preferences) AS entertainment,
        AVG(electronics_preferences) AS electronics,
        AVG(beauty_preferences) AS beauty,
        AVG(automative_preferences) AS automative,
        AVG(home_preferences) AS home,
        AVG(other_preferences) AS other
      FROM 
        users 
      WHERE 
        bluetoothCode IN (?)
    `;
  
    const [rows] = await con.query(query, [users]);
    if (!rows[0] || !rows[0].has_users) {
      return {status: false, message: "User not found or no data available"};
    }
      return {status: true, averages: rows[0]};
  }

  async put_advertiser(name, budget) {
    const query = "INSERT INTO advertisers (name, budget) VALUES (?, ?)"
    const [rows] = await con.query(query, [name, budget])
    return {status: true, rows: rows, message: "Advertiser added"}
  }

  async put_ad(adType, health_preferences, food_preferences, clothing_preferences, electronics_preferences, entertainment_preferences, beauty_preferences, home_preferences, automative_preferences, other_preferences, url, advertiserID, bid) {
    const query = "INSERT INTO ads (adType, health_preferences, food_preferences, clothing_preferences, electronics_preferences, entertainment_preferences, beauty_preferences, home_preferences, automative_preferences, other_preferences, url, advertiserID, bid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    const [rows] = await con.query(query, [adType, health_preferences, food_preferences, clothing_preferences, electronics_preferences, entertainment_preferences, beauty_preferences, home_preferences, automative_preferences, other_preferences, url, advertiserID, bid])
    return {status: true, message: "Ad added"}
  }

  async get_ads() {
    const query = "SELECT * FROM ads"
    const [rows] = await con.query(query)
    if (!rows[0]) return {status: false, message: "No ads found"}
    for (var i = 0; i < rows.length; i++) {
      var newObj = {}
      newObj.id = rows[i].id
      newObj.adType = rows[i].adType
      var preferences = {
        health: rows[i].health_preferences,
        food: rows[i].food_preferences,
        clothing: rows[i].clothing_preferences,
        electronics: rows[i].electronics_preferences,
        entertainment: rows[i].entertainment_preferences,
        beauty: rows[i].beauty_preferences,
        home: rows[i].home_preferences,
        automative: rows[i].automative_preferences,
        other: rows[i].other_preferences
      }
      newObj.preferences = preferences
      newObj.url = rows[i].url
      newObj.advertiserID = rows[i].advertiserID
      newObj.bid = rows[i].bid
      rows[i] = newObj
    }
    return {status: true, data: rows}
  }

}