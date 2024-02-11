# Use the official Nginx image as the base image
FROM nginx:alpine

# Copy the HTML file and Nginx configuration file
COPY inference-as-a-service.html /usr/share/nginx/html/
COPY default.conf /etc/nginx/conf.d/

# Expose port 80
EXPOSE 80

# Start Nginx when the container runs
CMD ["nginx", "-g", "daemon off;"]
