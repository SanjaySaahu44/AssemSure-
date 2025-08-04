import streamlit as st
import boto3
import os
from botocore.exceptions import ClientError

st.set_page_config(page_title="ASSEMSURE", layout="wide")
st.title("🤖 ASSEMSURE")
st.subheader("Real-time monitoring of robotic arm sensors from DynamoDB")

# AWS credentials (you’ll add them securely in Streamlit Cloud)
AWS_REGION = os.environ.get("AWS_REGION", "eu-north-1")
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE", "SensorData")

# Initialize DynamoDB
try:
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=AWS_REGION,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    table = dynamodb.Table(DYNAMODB_TABLE)
except Exception as e:
    st.error(f"❌ Error connecting to DynamoDB: {e}")
    st.stop()

# Load data
def fetch_data():
    try:
        response = table.scan()
        return response.get("Items", [])
    except ClientError as e:
        st.error(f"❌ Error reading data: {e.response['Error']['Message']}")
        return []

if st.button("🔄 Refresh Data"):
    st.experimental_rerun()

data = fetch_data()

# Display data
if not data:
    st.warning("No data available.")
else:
    st.markdown("### 📊 Sensor Data Table")
    st.dataframe(data, use_container_width=True)
