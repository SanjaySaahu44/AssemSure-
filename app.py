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
        
        # Ensure 'id' is the first key in each dictionary
        reordered_items = []
        for item in items:
            if "id" in item:
                reordered_item = {"id": item["id"]}
                for k, v in item.items():
                    if k != "id":
                        reordered_item[k] = v
                reordered_items.append(reordered_item)
            else:
                reordered_items.append(item)
                
        return reordered_items
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
    col1.metric("Torque", float(latest.get("torque", 0)))
    col2.metric("Current", float(latest.get("current", 0)))
    col3.metric("Vibration", float(latest.get("vibration", 0)))
    col4.metric("Label", str(latest.get("label", "N/A")))

    col5, col6 = st.columns(2)
    col5.metric("Temperature", float(latest.get("temperature", 0)))
    col6.metric("Noise", float(latest.get("noise", 0)))

    # Show full table
    st.markdown("### 📊 Complete Sensor Data")
    st.dataframe(data, use_container_width=True)
