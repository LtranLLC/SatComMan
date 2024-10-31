#!/bin/bash

# deploy_satcom.sh
# Deployment script for SatComMan on Ubuntu 24.04.1 LTS

set -e  # Exit immediately if a command exits with a non-zero status

# Function to display messages
function echo_info() {
    echo -e "\e[34m[INFO]\e[0m $1"
}

function echo_success() {
    echo -e "\e[32m[SUCCESS]\e[0m $1"
}

function echo_error() {
    echo -e "\e[31m[ERROR]\e[0m $1"
}

# Update and upgrade the system
echo_info "Updating and upgrading the system..."
sudo apt update -y && sudo apt upgrade -y

# Install essential dependencies
echo_info "Installing essential dependencies..."
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    software-properties-common

# Install Docker
echo_info "Installing Docker..."

# Add Docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up the stable repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update the package index
sudo apt update -y

# Install Docker Engine
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Verify Docker installation
echo_info "Verifying Docker installation..."
sudo docker --version

# Install Docker Compose
echo_info "Installing Docker Compose..."
DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep tag_name | cut -d '"' -f 4)
sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Apply executable permissions to the Docker Compose binary
sudo chmod +x /usr/local/bin/docker-compose

# Verify Docker Compose installation
echo_info "Verifying Docker Compose installation..."
docker-compose --version

# Add current user to the docker group
echo_info "Adding user '$USER' to the docker group..."
sudo usermod -aG docker $USER

# Inform the user to log out and back in
echo_success "Docker and Docker Compose have been installed successfully."
echo_info "Please log out and log back in to apply Docker group changes."

# Optional: Install Docker Compose via pip (if needed)
# Uncomment the following lines if you prefer using pip for Docker Compose
# echo_info "Installing Docker Compose using pip..."
# sudo apt install -y python3-pip
# sudo pip3 install docker-compose
# docker-compose --version

# Install Git (if not already installed)
echo_info "Ensuring Git is installed..."
sudo apt install -y git

# Clone the SatComMan repository
REPO_URL="https://github.com/yourusername/SatComMan.git"  # Replace with your repository URL
CLONE_DIR="$HOME/SatComMan"

echo_info "Cloning the SatComMan repository from $REPO_URL..."
if [ -d "$CLONE_DIR" ]; then
    echo_info "Repository already exists. Pulling the latest changes..."
    cd "$CLONE_DIR"
    git pull
else
    git clone "$REPO_URL" "$CLONE_DIR"
    cd "$CLONE_DIR"
fi

# Navigate to the project directory
cd "$CLONE_DIR"

# Prompt the user to enter environment variables or create a .env file
ENV_FILE=".env"

if [ ! -f "$ENV_FILE" ]; then
    echo_info "Creating a .env file for environment variables..."
    touch "$ENV_FILE"

    echo_info "Please enter the following environment variables:"

    read -p "SECRET_KEY: " SECRET_KEY
    read -p "WEBHOOK_API_KEY: " WEBHOOK_API_KEY
    read -p "MYSQL_ROOT_PASSWORD: " MYSQL_ROOT_PASSWORD
    read -p "MYSQL_USER: " MYSQL_USER
    read -p "MYSQL_PASSWORD: " MYSQL_PASSWORD
    read -p "MYSQL_DATABASE: " MYSQL_DATABASE

    cat <<EOL >> $ENV_FILE
# Backend Environment Variables
SECRET_KEY=$SECRET_KEY
WEBHOOK_API_KEY=$WEBHOOK_API_KEY

# MySQL Environment Variables
MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD
MYSQL_USER=$MYSQL_USER
MYSQL_PASSWORD=$MYSQL_PASSWORD
MYSQL_DATABASE=$MYSQL_DATABASE
EOL

    echo_success ".env file has been created successfully."
else
    echo_info ".env file already exists. Skipping creation."
fi

# Ensure Docker Compose uses the correct .env file
echo_info "Setting up Docker Compose environment variables..."
export $(grep -v '^#' .env | xargs)

# Run Docker Compose
echo_info "Starting Docker Compose services..."
sudo docker-compose up -d --build

echo_success "SatComMan has been deployed successfully!"

echo_info "Access the frontend at http://localhost:3000 and the backend API at http://localhost:8000"

# Optional: Print instructions for user to log out and back in for Docker group changes
echo_info "If you added your user to the docker group, please log out and log back in to apply the changes."
