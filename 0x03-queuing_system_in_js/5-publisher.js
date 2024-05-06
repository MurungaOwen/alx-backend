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

// Define the publishMessage function
function publishMessage(message, time) {
    setTimeout(() => {
      console.log(`About to send ${message}`);
      client.publish('holberton school channel', message);
    }, time);
  }

publishMessage("Holberton Student #1 starts course", 100);
publishMessage("Holberton Student #2 starts course", 200);
publishMessage("KILL_SERVER", 300);
publishMessage("Holberton Student #3 starts course", 400)
