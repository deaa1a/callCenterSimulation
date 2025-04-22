## Setup Instructions

### Step 1: Set Up the Database

The application uses PostgreSQL as its database. Use Docker to set it up:

1. Build the Docker image:

```
docker build -t postgres-call-center .
```

2. Run the container:

```
docker run -d --name postgres-container-call-center -p 5432:5432 postgres-call-center
```

---