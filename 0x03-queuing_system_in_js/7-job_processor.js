import { createQueue } from "kue";

const queue = createQueue({
    concurrency: 2 // Process two jobs at a time
  });

const blackListedNumbers = [ '4153518780', '4153518781' ];

// Function to send notification
function sendNotification(phoneNumber, message, job, done) {
    job.progress(0, 100); // Track progress of the job
  
    if (blackListedNumbers.includes(phoneNumber)) {
      // Mark the job as failed with an error
      done(new Error(`Phone number ${phoneNumber} is blacklisted`));
    } else {
      // Simulating sending notification
      let progress = 0;
      const interval = setInterval(() => {
        progress += 10;
        job.progress(progress, 100);
        if (progress >= 50) {
          clearInterval(interval);
          console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
          job.progress(50, 100); // Update progress to 50%
          done();
        }
      }, 500);
    }
  }
  
  
queue.process('push_notification_code_2', 2, (job, done) => {
    const { phoneNumber, message } = job.data;
    sendNotification(phoneNumber, message, job, done);
  });