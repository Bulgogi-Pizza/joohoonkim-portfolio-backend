"""
S3 utility functions for file upload and management
"""
import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from typing import Optional
from fastapi import UploadFile
import uuid

# S3 Configuration from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-2")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "amplify-d1jx5u7u0ebuxt-ma-amplifydataamplifycodege-0fxenzrmrqkf")
S3_PREFIX = os.getenv("S3_PREFIX", "joohoonkim/portfolio/")

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate a unique filename with timestamp and UUID
    """
    ext = original_filename.rsplit('.', 1)[-1] if '.' in original_filename else ''
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}.{ext}" if ext else f"{timestamp}_{unique_id}"


async def upload_file_to_s3(
    file: UploadFile,
    folder: str = ""
) -> str:
    """
    Upload a file to S3 and return the public URL
    
    Args:
        file: FastAPI UploadFile object
        folder: Subfolder within S3_PREFIX (e.g., 'icons', 'profiles', 'cover-arts')
    
    Returns:
        Public S3 URL of the uploaded file
    """
    try:
        # Generate unique filename
        filename = generate_unique_filename(file.filename or "file")
        
        # Construct S3 key
        s3_key = f"{S3_PREFIX}{folder}/{filename}" if folder else f"{S3_PREFIX}{filename}"
        
        # Read file content
        file_content = await file.read()
        
        # Upload to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=file_content,
            ContentType=file.content_type or 'application/octet-stream'
        )
        
        # Generate public URL
        s3_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
        
        return s3_url
        
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_message = e.response.get('Error', {}).get('Message', str(e))
        print(f"S3 ClientError: {error_code} - {error_message}")
        print(f"Bucket: {S3_BUCKET_NAME}, Region: {AWS_REGION}, Key: {s3_key}")
        raise Exception(f"Failed to upload file to S3: {error_code} - {error_message}")
    except Exception as e:
        print(f"S3 Upload Error: {type(e).__name__}: {str(e)}")
        raise Exception(f"Error uploading file: {str(e)}")


def delete_file_from_s3(file_url: str) -> bool:
    """
    Delete a file from S3 given its URL
    
    Args:
        file_url: Full S3 URL of the file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Extract S3 key from URL
        # Example URL: https://bucket.s3.region.amazonaws.com/key
        if S3_BUCKET_NAME in file_url:
            # Extract the key part after the bucket URL
            parts = file_url.split(f"{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/")
            if len(parts) > 1:
                s3_key = parts[1]
                
                # Delete from S3
                s3_client.delete_object(
                    Bucket=S3_BUCKET_NAME,
                    Key=s3_key
                )
                return True
        
        return False
        
    except ClientError as e:
        print(f"Error deleting file from S3: {str(e)}")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def get_s3_file_url(s3_key: str) -> str:
    """
    Generate public S3 URL from S3 key
    
    Args:
        s3_key: S3 object key
    
    Returns:
        Public S3 URL
    """
    return f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
