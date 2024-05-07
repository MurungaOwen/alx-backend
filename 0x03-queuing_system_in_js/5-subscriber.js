import redis from "redis"

// initialise client
const client = redis.createClient();

// if error occurs
client.on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err}`);
});

// Event listener for successful connection
client.on('connect', () => {
    console.log('Redis client connected to the server');
  });

// subscribe to Holberton school
client.subscribe('holberton school channel');

// if message sent by subscriber
client.on('message', (message) => {
    if (message === "KILL_SERVER") {
        console.log(message)
        client.unsubscribe();
        client.quit();
    } else {
        console.log(message);
    }
});