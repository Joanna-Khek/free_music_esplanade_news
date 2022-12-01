import cron from 'node-cron';

cron.schedule(`0 * * * *`, async () => {
  console.log('running your task...');
});