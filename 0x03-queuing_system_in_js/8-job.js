function createPushNotificationsJobs(jobs, queue) {
    if(!Array.isArray(jobs)) {
        throw new Error('Jobs is not an array');
    } else {
        jobs.forEach((val) => {
            const job = queue.create('push_notification_code_3', val).save((err) => {
                if(!err) {
                    console.log(`Notification job created: ${job.id}`);
                }
            });

            job.on('complete', () => {
                console.log(`Notification job ${job.id} completed`);
            });
            
            job.on('failed', (err) => {
                console.log(`Notification job ${job.id} failed: ${err}`);
            });
            
            job.on('progress', (progress) => {
                console.log(`Notification job ${job.id} ${progress}% complete`);
            });
        });
    }
}

module.exports = createPushNotificationsJobs