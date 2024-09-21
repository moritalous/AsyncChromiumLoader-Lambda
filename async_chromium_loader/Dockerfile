# https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-clients

# Define custom function directory
ARG FUNCTION_DIR="/function"

# Use a slim version of the base Python image to reduce the final image size
FROM python:3.12-slim

# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Copy function code
RUN mkdir -p ${FUNCTION_DIR}
COPY requirements.txt ${FUNCTION_DIR}

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Install the function's dependencies
RUN pip install -r requirements.txt && \
    playwright install --with-deps chromium

COPY app.py ${FUNCTION_DIR}

# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
# Pass the name of the function handler as an argument to the runtime
CMD [ "app.lambda_handler" ]
