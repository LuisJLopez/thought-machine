FROM python:3.9.5

# # Set working directory
WORKDIR /project

COPY requirements.txt requirements.txt

# Install packages (only pytest)
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run
CMD ["python", "project", "inputs/input.txt"]