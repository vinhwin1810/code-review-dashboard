FROM node:16-buster-slim

# Set the working directory
WORKDIR /app

# Add `package.json` and `package-lock.json` (if available)
ADD package*.json ./

ENV REACT_APP_API_URL=http://127.0.0.1:8000

# Install dependencies
RUN npm install

# Copy application files
COPY . .

# Build the application
RUN npm run build

# Install serve to run the application
RUN npm install -g serve


# Run the application on port 3000
CMD ["serve", "-s", "build", "-l", "3000"]