const createPushNotificationsJobs = require('./8-job');
const kue = require('kue');
const redis = require('redis');
const assert = require('assert');

describe('createPushNotificationsJobs', () => {
  let queue;

  // Create a Redis client
  const client = redis.createClient();

  beforeEach(() => {
    // Use the client to create the Kue queue in test mode
    queue = kue.createQueue({ redis: client, testMode: true });
  });

  afterEach((done) => {
    // Clear the queue and exit test mode after each test
    queue.testMode.clear(done);
    queue.testMode.exit();
  });

  it('should create jobs for each notification', (done) => {
    const notifications = [
      {
        phoneNumber: '123',
        message: 'Message 1',
      },
      {
        phoneNumber: '456',
        message: 'Message 2',
      },
      {
        phoneNumber: '789',
        message: 'Message 3',
      },
    ];

    createPushNotificationsJobs(notifications, queue);

    // Wait for the jobs to be processed
    setTimeout(() => {
      // Assert that jobs are created in the queue
      assert.strictEqual(queue.testMode.jobs.length, notifications.length);

      // Assert that each job has correct data
      notifications.forEach((notification, index) => {
        const job = queue.testMode.jobs[index];
        assert.strictEqual(job.type, 'push_notification_code_3');
        assert.deepStrictEqual(job.data, notification);
      });

      done();
    }, 1000); // Adjust timeout as needed
  });

  it('should handle empty notifications array', (done) => {
    createPushNotificationsJobs([], queue);

    // Wait for the jobs to be processed
    setTimeout(() => {
      // Assert that no jobs are created in the queue
      assert.strictEqual(queue.testMode.jobs.length, 0);

      done();
    }, 1000); // Adjust timeout as needed
  });
});
