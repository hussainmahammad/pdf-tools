
FROM public.ecr.aws/lambda/nodejs:20

# Dummy image to simulate Lambda container
COPY app/backend/lambda-handler.js ${LAMBDA_TASK_ROOT}

CMD ["lambda-handler.handler"]
