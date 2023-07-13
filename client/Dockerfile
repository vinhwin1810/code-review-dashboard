FROM node:16-buster-slim

# Set the working directory
WORKDIR /app

# Add `package.json` and `package-lock.json` (if available)
ADD package*.json ./

# Install dependencies
RUN npm install

# Copy application files
COPY . .

# Build the application
RUN npm run build

# Install serve to run the application
RUN npm install -g serve

ENV REACT_APP_API_URL=http://127.0.0.1:5000
# Run the application on port 5000
CMD ["serve", "-s", "build", "-l", "5000"]