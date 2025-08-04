import streamlit as st
import boto3
import os
from botocore.exceptions import ClientError

st.set_page_config(page_title="ASSEMSURE", layout="wide")
st.title("🤖 ASSEMSURE")
st.subheader("Real-time monitoring of robotic arm sensors from DynamoDB")

# AWS config
AWS_REGION = os.environ.get("AWS_REGION", "eu-north-1")
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE", "RobotSensorData")

# Connect to DynamoDB
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

# Fetch data
def fetch_data():
    try:
        response = table.scan()
        items = response.get("Items", [])
        # Move 'id' to the first column
        for item in items:
            item.move_to_end("id", last=False)
        return items
    except ClientError as e:
        st.error(f"❌ Error reading data: {e.response['Error']['Message']}")
        return []

# Load and display data
data = fetch_data()

if not data:
    st.warning("No data available.")
else:
    latest = data[-1]  # Show most recent data

    # Show latest individual sensor values
    st.markdown("### 📟 Latest Sensor Values")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Torque", latest.get("torque"))
    col2.metric("Current", latest.get("current"))
    col3.metric("Vibration", latest.get("vibration"))
    col4.metric("Label", latest.get("label"))

    # Show full table
    st.markdown("### 📊 Complete Sensor Data")
    st.dataframe(data, use_container_width=True)
