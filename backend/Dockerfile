FROM public.ecr.aws/lambda/python:3.9


# Install pip packages
COPY requirements.txt .
RUN pip install -r requirements.txt  --target "${LAMBDA_TASK_ROOT}"

# Copy the Flask app files into the container
COPY webapp/ ${LAMBDA_TASK_ROOT}/
RUN ls -la /${LAMBDA_TASK_ROOT}/*

# Running in AWS: Start the Flask app
CMD [ "api.aws_lambda_handler" ]