import streamlit as st
import app_lib as glib

# Streamlit UI 설정
st.set_page_config(page_title="Predictive AICC", layout="wide")
st.title("Predictive AICC")

# 왼쪽 사이드바 구성
with st.sidebar:
    st.header("Input Parameters")
    model_id = st.text_input("Model ID", "")
    customer_id = st.text_input("Customer ID", "")
    analyze_button = st.button("Analyze", type="primary")
    
    # 모델 ID 예시 표시
    st.markdown("---")
    st.subheader("Available Model IDs:")
    st.code("anthropic.claude-3-sonnet-20240229-v1:0")
    st.code("us.amazon.nova-lite-v1:0")

    st.subheader("Available Customer IDs:")
    st.code("S5_20984")

# 메인 화면 구성
if analyze_button and customer_id and model_id:
    # Customer Events 섹션
    events = glib.get_customer_events(customer_id)
    if events:
        st.subheader("Customer Events:")
        for event in events:
            st.write(f"Date: {event['date']}, Event: {event['type']}")
        
        # Predictive Analysis 섹션
        st.subheader("Predictive Analysis:")
        response_placeholder = st.empty()
        
        def streaming_callback(chunk):
            if not hasattr(st.session_state, 'response_text'):
                st.session_state.response_text = ""
            st.session_state.response_text += chunk
            response_placeholder.markdown(st.session_state.response_text)
        
        # get_streaming_response 호출 시 model_id 전달
        glib.get_streaming_response(events, streaming_callback,model_id)
