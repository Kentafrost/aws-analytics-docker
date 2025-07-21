FROM public.ecr.aws/lambda/python:3.12
LABEL version="1.0"
LABEL description="AWS Lambda Python 3.12 Example"

# LAMBDA_TASK_ROOT ⇒ Lambdaの環境変数でapp.pyをLambda関数に渡す
COPY app.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Lambda起動時に実行するメソッドを指定
CMD ["app.handler"]