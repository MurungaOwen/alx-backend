const kue = require('kue');
const chai = require('chai');
const sinon = require('sinon');
const createPushNotificationsJobs = require('./8-job');

// Use chai expect syntax
const expect = chai.expect;

describe('createPushNotificationsJobs', () => {
  let queueStub;

  beforeEach(() => {
    // Create a stub for the Kue queue
    queueStub = {
      create: sinon.stub().returnsThis(), // Stub create method
      save: sinon.stub().callsFake((callback) => callback()), // Stub save method
      on: sinon.stub(), // Stub on method
    };
  });

  it('should throw an error if jobs is not an array', () => {
    expect(() => {
      createPushNotificationsJobs({}, queueStub);
    }).to.throw('Jobs is not an array');
  });

  it('should create jobs and save them to the queue', () => {
    const jobs = [
      { data: { message: 'Job 1' } },
      { data: { message: 'Job 2' } },
      { data: { message: 'Job 3' } },
    ];

    // Call the function
    createPushNotificationsJobs(jobs, queueStub);

    // Ensure that the create and save methods were called for each job
    jobs.forEach((jobData) => {
      // Ensure that create method is called with proper data
      expect(queueStub.create.calledWith('push_notification_code_3', jobData)).to.be.true;
      // Ensure that save method is called after create
      expect(queueStub.save.calledAfter(queueStub.create)).to.be.true;

      // Get the callback function passed to create method
      const saveCallback = queueStub.create.args[0][0];

      // Simulate job completion
      saveCallback(null);
    });
  });

  // Add more test cases as needed
});
