import streamlit as st
import boto3
from boto3.dynamodb.conditions import Key

def process_customer_events(customer_id,streaming_callback):
    """고객 이벤트 처리 및 분석"""
    # 고객 이벤트 조회
    events = get_customer_events(customer_id)
    
    if events:
        #display_events(events)
        get_streaming_response(events,streaming_callback)
    else:
        st.warning(f"No events found for customer ID: {customer_id}")

def get_streaming_response(events, streaming_callback, model_id):
    """Claude/Nova API로부터 스트리밍 응답을 받아 처리합니다."""
    #st.subheader("Predictive Analysis:")

    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')
    
    events_text = "\n".join([f"Date: {event['date']}, Event: {event['type']}" 
                        for event in events])
    
    analysis_prompt = f"""
    Customer Events:
    {events_text}
    Based on the customer events, predict the reason code for the call and give a detailed explanation of why you think that in Korean.
    """

    message = {
        "role": "user",
        "content": [{"text": analysis_prompt}]
    }
    
    response = bedrock.converse_stream(
        modelId=model_id,
        messages=[message],
        inferenceConfig={
            "maxTokens": 2000,
            "temperature": 0.0
        }
    )
    
    stream = response.get('stream')
    for event in stream:
        if "contentBlockDelta" in event:
            streaming_callback(event['contentBlockDelta']['delta']['text'])


def get_customer_events(customer_id):
    """DynamoDB에서 고객 이벤트 데이터를 가져옵니다."""
    try:
        table = boto3.resource('dynamodb').Table('CustomerOrders')
        response = table.query(
            KeyConditionExpression=Key('customer_id').eq(customer_id),
            ScanIndexForward=True  # 날짜순 정렬
        )
        return response['Items']
    except Exception as e:
        st.error(f"Error querying DynamoDB: {str(e)}")
        return []

