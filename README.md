---
date: 2024-04-15T13:32:38.000978
author: AutoGPT <info@agpt.co>
---

# Image Resizing API

The project involves developing a feature that accepts an image file and desired dimensions, then resizes the image to fit within those specifications, with the option to crop the image to maintain the aspect ratio or to add padding to fit the specified dimensions without cropping. Key preferences and requirements include: - The use of PNG format for its support of transparency and the ability to maintain high image quality after compression and resizing. - Desired dimensions are set at 1280x720 pixels, chosen for its balance between quality and file size, suitable for both online viewing and moderate-quality printing. - Keeping the original aspect ratio of the image is essential to avoid stretching or squashing, maintaining the visual fidelity of the original image. - When adjusting the aspect ratio, padding is preferred over cropping to ensure no part of the image is lost, maintaining the integrity of the visual content. The tech stack for this project includes Python as the programming language, FastAPI for the API framework, PostgreSQL for the database, and Prisma as the ORM. This stack supports the development of high-performance, scalable applications, and ensures efficient database management and seamless deployment of web services.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'Image Resizing API'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
