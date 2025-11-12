# Message Queue Setup - Bull & BullMQ

**For:** Node.js async job processing  
**Coverage:** Job queues, workers, scheduling, retry logic  
**Tools:** Bull/BullMQ 4+, Redis, Bull Board (monitoring)

---

## 📦 Installation

```bash
# Bull (stable, battle-tested)
npm install bull

# BullMQ (modern, TypeScript-first)
npm install bullmq

# UI Dashboard
npm install bull-board @bull-board/express

# Types
npm install -D @types/bull
```

---

## 📂 Project Structure

```
backend/
├── src/
│   ├── queues/
│   │   ├── index.ts           # Queue registry
│   │   ├── email.queue.ts     # Email queue
│   │   ├── image.queue.ts     # Image processing
│   │   └── report.queue.ts    # Report generation
│   ├── workers/
│   │   ├── email.worker.ts    # Email processor
│   │   ├── image.worker.ts    # Image processor
│   │   └── report.worker.ts   # Report processor
│   ├── jobs/
│   │   ├── email.jobs.ts      # Job creators
│   │   └── types.ts           # Job types
│   └── config/
│       └── queue.config.ts    # Queue configuration
└── worker.ts                  # Worker entry point
```

---

## ⚙️ Queue Configuration

### config/queue.config.ts

```typescript
import { QueueOptions } from 'bull';

export const queueConfig: QueueOptions = {
  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
    password: process.env.REDIS_PASSWORD,
  },
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
    removeOnComplete: 100, // Keep last 100 completed jobs
    removeOnFail: 500,     // Keep last 500 failed jobs
  },
};

// BullMQ configuration
import { ConnectionOptions } from 'bullmq';

export const bullMQConfig: ConnectionOptions = {
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  password: process.env.REDIS_PASSWORD,
};
```

---

## 📝 Queue Setup (Bull)

### queues/email.queue.ts

```typescript
import Queue, { Job } from 'bull';
import { queueConfig } from '../config/queue.config';

export interface SendEmailJob {
  to: string;
  subject: string;
  template: string;
  data: Record<string, any>;
  priority?: number;
}

export const emailQueue = new Queue<SendEmailJob>('email', queueConfig);

// Add job to queue
export async function sendEmail(data: SendEmailJob) {
  return emailQueue.add(data, {
    priority: data.priority || 1,
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 5000,
    },
  });
}

// Bulk add jobs
export async function sendBulkEmails(emails: SendEmailJob[]) {
  const jobs = emails.map(email => ({
    data: email,
    opts: {
      priority: email.priority || 1,
    },
  }));

  return emailQueue.addBulk(jobs);
}

// Schedule delayed email
export async function scheduleEmail(data: SendEmailJob, delay: number) {
  return emailQueue.add(data, {
    delay, // milliseconds
  });
}

// Recurring job (cron)
export async function setupRecurringEmail() {
  return emailQueue.add(
    {
      to: 'admin@example.com',
      subject: 'Daily Report',
      template: 'daily-report',
      data: {},
    },
    {
      repeat: {
        cron: '0 9 * * *', // Every day at 9 AM
      },
    }
  );
}

// Queue events
emailQueue.on('completed', (job: Job, result) => {
  console.log(`✅ Email job ${job.id} completed:`, result);
});

emailQueue.on('failed', (job: Job, error) => {
  console.error(`❌ Email job ${job.id} failed:`, error.message);
});

emailQueue.on('progress', (job: Job, progress: number) => {
  console.log(`📊 Email job ${job.id} progress: ${progress}%`);
});

emailQueue.on('stalled', (job: Job) => {
  console.warn(`⚠️ Email job ${job.id} stalled`);
});
```

### queues/image.queue.ts

```typescript
import Queue from 'bull';
import { queueConfig } from '../config/queue.config';

export interface ProcessImageJob {
  imageUrl: string;
  userId: string;
  operations: {
    resize?: { width: number; height: number };
    compress?: { quality: number };
    watermark?: { text: string };
  };
}

export const imageQueue = new Queue<ProcessImageJob>('image-processing', {
  ...queueConfig,
  limiter: {
    max: 5, // Max 5 jobs
    duration: 1000, // per second
  },
});

export async function processImage(data: ProcessImageJob) {
  return imageQueue.add(data, {
    attempts: 5,
    priority: 2,
    timeout: 30000, // 30 seconds timeout
  });
}

// Named jobs for different priorities
export async function processImageUrgent(data: ProcessImageJob) {
  return imageQueue.add('urgent', data, {
    priority: 1, // Higher priority (lower number = higher priority)
  });
}
```

### queues/report.queue.ts

```typescript
import Queue from 'bull';
import { queueConfig } from '../config/queue.config';

export interface GenerateReportJob {
  reportType: 'sales' | 'analytics' | 'users';
  startDate: Date;
  endDate: Date;
  userId: string;
  format: 'pdf' | 'xlsx' | 'csv';
}

export const reportQueue = new Queue<GenerateReportJob>('reports', queueConfig);

export async function generateReport(data: GenerateReportJob) {
  return reportQueue.add(data, {
    attempts: 2,
    timeout: 300000, // 5 minutes
  });
}
```

---

## 👷 Workers (Job Processors)

### workers/email.worker.ts

```typescript
import { Job } from 'bull';
import { emailQueue, SendEmailJob } from '../queues/email.queue';
import nodemailer from 'nodemailer';

// Email transporter
const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: parseInt(process.env.SMTP_PORT || '587'),
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

// Process email jobs
emailQueue.process(async (job: Job<SendEmailJob>) => {
  const { to, subject, template, data } = job.data;

  console.log(`📧 Processing email job ${job.id}: ${to}`);

  try {
    // Update progress
    await job.progress(10);

    // Render email template
    const html = await renderEmailTemplate(template, data);
    await job.progress(40);

    // Send email
    const result = await transporter.sendMail({
      from: process.env.SMTP_FROM,
      to,
      subject,
      html,
    });

    await job.progress(100);

    console.log(`✅ Email sent to ${to}:`, result.messageId);

    return {
      success: true,
      messageId: result.messageId,
      to,
    };
  } catch (error) {
    console.error(`❌ Failed to send email to ${to}:`, error);
    throw error; // Will trigger retry
  }
});

// Render email template
async function renderEmailTemplate(
  template: string,
  data: Record<string, any>
): Promise<string> {
  // Load and render template (use your template engine)
  return `<html><body>Email content for ${template}</body></html>`;
}
```

### workers/image.worker.ts

```typescript
import { Job } from 'bull';
import { imageQueue, ProcessImageJob } from '../queues/image.queue';
import sharp from 'sharp';
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import axios from 'axios';

const s3Client = new S3Client({ region: process.env.AWS_REGION });

// Process with concurrency
imageQueue.process(5, async (job: Job<ProcessImageJob>) => {
  const { imageUrl, operations, userId } = job.data;

  console.log(`🖼️ Processing image job ${job.id}: ${imageUrl}`);

  try {
    // Download image
    await job.progress(10);
    const response = await axios.get(imageUrl, {
      responseType: 'arraybuffer',
    });
    const imageBuffer = Buffer.from(response.data);

    await job.progress(30);

    // Process image with sharp
    let image = sharp(imageBuffer);

    if (operations.resize) {
      image = image.resize(operations.resize.width, operations.resize.height);
    }

    if (operations.compress) {
      image = image.jpeg({ quality: operations.compress.quality });
    }

    await job.progress(60);

    // Convert to buffer
    const processedBuffer = await image.toBuffer();

    await job.progress(80);

    // Upload to S3
    const key = `processed/${userId}/${Date.now()}.jpg`;
    await s3Client.send(
      new PutObjectCommand({
        Bucket: process.env.S3_BUCKET,
        Key: key,
        Body: processedBuffer,
        ContentType: 'image/jpeg',
      })
    );

    await job.progress(100);

    const resultUrl = `https://${process.env.S3_BUCKET}.s3.amazonaws.com/${key}`;

    console.log(`✅ Image processed: ${resultUrl}`);

    return {
      success: true,
      url: resultUrl,
      originalUrl: imageUrl,
    };
  } catch (error) {
    console.error(`❌ Image processing failed:`, error);
    throw error;
  }
});

// Named job processor (urgent)
imageQueue.process('urgent', 10, async (job) => {
  console.log(`🚨 Processing URGENT image job ${job.id}`);
  // Same processing logic but higher priority
});
```

### workers/report.worker.ts

```typescript
import { Job } from 'bull';
import { reportQueue, GenerateReportJob } from '../queues/report.queue';
import PDFDocument from 'pdfkit';
import ExcelJS from 'exceljs';

reportQueue.process(async (job: Job<GenerateReportJob>) => {
  const { reportType, startDate, endDate, userId, format } = job.data;

  console.log(`📊 Generating ${reportType} report for user ${userId}`);

  try {
    await job.progress(10);

    // Fetch data
    const data = await fetchReportData(reportType, startDate, endDate);
    await job.progress(40);

    // Generate report based on format
    let fileBuffer: Buffer;
    let mimeType: string;

    switch (format) {
      case 'pdf':
        fileBuffer = await generatePDFReport(data);
        mimeType = 'application/pdf';
        break;
      case 'xlsx':
        fileBuffer = await generateExcelReport(data);
        mimeType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
        break;
      case 'csv':
        fileBuffer = Buffer.from(generateCSVReport(data));
        mimeType = 'text/csv';
        break;
    }

    await job.progress(80);

    // Upload to S3 or save
    const reportUrl = await uploadReport(fileBuffer, userId, format);

    await job.progress(100);

    console.log(`✅ Report generated: ${reportUrl}`);

    // Notify user
    await notifyUser(userId, reportUrl);

    return {
      success: true,
      reportUrl,
      reportType,
      format,
    };
  } catch (error) {
    console.error('❌ Report generation failed:', error);
    throw error;
  }
});

async function fetchReportData(type: string, start: Date, end: Date) {
  // Fetch from database
  return {};
}

async function generatePDFReport(data: any): Promise<Buffer> {
  return new Promise((resolve, reject) => {
    const doc = new PDFDocument();
    const chunks: Buffer[] = [];

    doc.on('data', chunks.push.bind(chunks));
    doc.on('end', () => resolve(Buffer.concat(chunks)));
    doc.on('error', reject);

    doc.text('Report Content', 100, 100);
    doc.end();
  });
}

async function generateExcelReport(data: any): Promise<Buffer> {
  const workbook = new ExcelJS.Workbook();
  const sheet = workbook.addWorksheet('Report');

  sheet.addRow(['Column 1', 'Column 2']);
  // Add data rows

  return await workbook.xlsx.writeBuffer() as Buffer;
}

function generateCSVReport(data: any): string {
  return 'Column1,Column2\nValue1,Value2';
}

async function uploadReport(buffer: Buffer, userId: string, format: string): Promise<string> {
  // Upload to S3 or file storage
  return `https://example.com/reports/${userId}.${format}`;
}

async function notifyUser(userId: string, reportUrl: string) {
  // Send notification/email
}
```

---

## 🚀 Worker Entry Point

### worker.ts

```typescript
import { emailQueue } from './queues/email.queue';
import { imageQueue } from './queues/image.queue';
import { reportQueue } from './queues/report.queue';

// Import workers
import './workers/email.worker';
import './workers/image.worker';
import './workers/report.worker';

console.log('🚀 Workers started');

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('Shutting down workers...');

  await Promise.all([
    emailQueue.close(),
    imageQueue.close(),
    reportQueue.close(),
  ]);

  console.log('Workers closed');
  process.exit(0);
});

// Error handling
process.on('uncaughtException', (error) => {
  console.error('Uncaught exception:', error);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled rejection at:', promise, 'reason:', reason);
  process.exit(1);
});
```

### package.json scripts

```json
{
  "scripts": {
    "dev": "ts-node src/server.ts",
    "worker": "ts-node src/worker.ts",
    "dev:worker": "nodemon --exec ts-node src/worker.ts"
  }
}
```

---

## 📊 Bull Board (Monitoring UI)

### Setup Dashboard

```typescript
import express from 'express';
import { createBullBoard } from '@bull-board/api';
import { BullAdapter } from '@bull-board/api/bullAdapter';
import { ExpressAdapter } from '@bull-board/express';
import { emailQueue, imageQueue, reportQueue } from './queues';

const app = express();

// Setup Bull Board
const serverAdapter = new ExpressAdapter();
serverAdapter.setBasePath('/admin/queues');

createBullBoard({
  queues: [
    new BullAdapter(emailQueue),
    new BullAdapter(imageQueue),
    new BullAdapter(reportQueue),
  ],
  serverAdapter,
});

app.use('/admin/queues', serverAdapter.getRouter());

app.listen(3000, () => {
  console.log('Bull Board running at http://localhost:3000/admin/queues');
});
```

---

## 🎯 Advanced Patterns

### Job Priorities

```typescript
// Low priority (background job)
await emailQueue.add(data, { priority: 10 });

// Normal priority
await emailQueue.add(data, { priority: 5 });

// High priority (urgent)
await emailQueue.add(data, { priority: 1 });
```

### Job Dependencies (Sequential Jobs)

```typescript
// Job 2 waits for Job 1 to complete
const job1 = await emailQueue.add('step1', data1);
const job2 = await emailQueue.add('step2', data2, {
  jobId: `parent-${job1.id}`,
});
```

### Rate Limiting

```typescript
const queue = new Queue('limited', {
  ...queueConfig,
  limiter: {
    max: 10,      // Max 10 jobs
    duration: 1000, // per 1 second
  },
});
```

### Job Lifecycle Events

```typescript
// Job events
job.on('progress', (progress) => {
  console.log(`Progress: ${progress}%`);
});

job.on('completed', (result) => {
  console.log('Completed:', result);
});

job.on('failed', (error) => {
  console.error('Failed:', error);
});

// Global queue events
queue.on('global:completed', (jobId, result) => {
  console.log(`Job ${jobId} completed globally`);
});

queue.on('global:failed', (jobId, error) => {
  console.error(`Job ${jobId} failed globally`);
});
```

### Retry Logic

```typescript
await queue.add(data, {
  attempts: 5,
  backoff: {
    type: 'exponential',
    delay: 2000, // Start with 2s, then 4s, 8s, 16s, 32s
  },
});

// Custom backoff
await queue.add(data, {
  attempts: 3,
  backoff: {
    type: 'fixed',
    delay: 5000, // Fixed 5s delay between retries
  },
});
```

### Cleanup Old Jobs

```typescript
// Auto cleanup on queue
const queue = new Queue('emails', {
  ...queueConfig,
  defaultJobOptions: {
    removeOnComplete: 100,  // Keep last 100 completed
    removeOnFail: 500,      // Keep last 500 failed
  },
});

// Manual cleanup
async function cleanupOldJobs() {
  // Remove completed jobs older than 1 day
  await queue.clean(24 * 3600 * 1000, 'completed');

  // Remove failed jobs older than 7 days
  await queue.clean(7 * 24 * 3600 * 1000, 'failed');
}
```

---

## 📈 Monitoring & Metrics

### Queue Metrics

```typescript
// Get queue metrics
async function getQueueMetrics(queue: Queue) {
  const [waiting, active, completed, failed, delayed] = await Promise.all([
    queue.getWaitingCount(),
    queue.getActiveCount(),
    queue.getCompletedCount(),
    queue.getFailedCount(),
    queue.getDelayedCount(),
  ]);

  return {
    waiting,
    active,
    completed,
    failed,
    delayed,
    total: waiting + active + completed + failed + delayed,
  };
}

// Get job counts
const metrics = await getQueueMetrics(emailQueue);
console.log('Queue metrics:', metrics);
```

### Job Inspection

```typescript
// Get job by ID
const job = await queue.getJob(jobId);

// Get job state
const state = await job.getState();

// Get job progress
const progress = job.progress();

// Get job logs
const logs = await queue.getJobLogs(jobId);
```

---

## 🧪 Testing

```typescript
import { emailQueue, sendEmail } from '../queues/email.queue';

describe('Email Queue', () => {
  beforeEach(async () => {
    await emailQueue.empty();
  });

  afterAll(async () => {
    await emailQueue.close();
  });

  it('should add job to queue', async () => {
    const job = await sendEmail({
      to: 'test@example.com',
      subject: 'Test',
      template: 'test',
      data: {},
    });

    expect(job.id).toBeDefined();
    expect(job.data.to).toBe('test@example.com');
  });

  it('should process job successfully', async () => {
    const job = await sendEmail({
      to: 'test@example.com',
      subject: 'Test',
      template: 'test',
      data: {},
    });

    // Wait for job completion
    const result = await job.finished();

    expect(result.success).toBe(true);
    expect(result.to).toBe('test@example.com');
  });
});
```

---

## ✅ Best Practices

1. **Separate Workers:** Run workers in separate processes
2. **Job Data:** Keep job data small, use references
3. **Idempotency:** Make jobs idempotent
4. **Error Handling:** Always catch and log errors
5. **Monitoring:** Use Bull Board for visibility
6. **Cleanup:** Remove old completed/failed jobs
7. **Priorities:** Use priorities appropriately
8. **Timeouts:** Set job timeouts
9. **Retry Logic:** Implement exponential backoff
10. **Testing:** Test job processors thoroughly

---

## 🐛 Common Issues

**Issue:** Jobs stuck in active state  
**Fix:** Set timeout, implement stalled job handler

**Issue:** Memory leak  
**Fix:** Remove completed jobs, use removeOnComplete

**Issue:** Jobs not processing  
**Fix:** Check worker is running, verify Redis connection

**Issue:** Slow processing  
**Fix:** Increase concurrency, scale workers horizontally

---

## 🚀 Production Deployment

```bash
# Run multiple workers with PM2
pm2 start worker.ts -i 4 --name "queue-worker"

# Monitor workers
pm2 monit

# Scale workers
pm2 scale queue-worker 8
```

---

**Ready for:** Async job processing at scale  
**Next:** Monitor jobs at `/admin/queues`
