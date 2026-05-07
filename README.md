# ☁️ CloudStore — Serverless Cloud Storage App

A production-grade serverless cloud storage application 
built on AWS from scratch — similar to Google Drive.

## 🌐 Live Demo
http://cloudstore-frontend-yourname.s3-website.ap-south-1.amazonaws.com

## ✨ Features
- 🔐 User authentication (signup, login, email verification)
- 📤 File upload & download via S3 presigned URLs
- 📁 Folder organization system
- 🔗 Shareable file links with 7-day expiry
- 📊 Real-time dashboard with storage stats

## 🏗️ Architecture
![Architecture](architecture.png)

## ⚙️ AWS Services Used
| Service | Purpose |
|---|---|
| S3 | File storage + frontend hosting |
| Cognito | User auth + JWT tokens |
| Lambda (Python) | Serverless backend logic |
| API Gateway | REST API with auth |
| DynamoDB | File metadata storage |

## 🚀 How It Works
1. User signs up → Cognito sends verification email
2. User logs in → Cognito returns JWT token
3. User uploads file → Lambda generates S3 presigned URL
4. Browser uploads directly to S3 (Lambda never touches file bytes)
5. File metadata saved to DynamoDB
6. User can download, delete, or share files

## 📁 Project Structure
\`\`\`
cloudstore-aws/
├── frontend/
│   └── index.html
├── backend/
│   ├── lambda_upload.py
│   ├── lambda_list.py
│   ├── lambda_download.py
│   ├── lambda_delete.py
│   └── lambda_share.py
└── README.md
\`\`\`

## 🛠️ Setup
1. Clone this repo
2. Deploy each Lambda function in AWS
3. Create API Gateway with Cognito authorizer
4. Update CONFIG in frontend/index.html
5. Host frontend on S3 static hosting

## 👨‍💻 Built By
Manushanth — CSE Student, Bangalore