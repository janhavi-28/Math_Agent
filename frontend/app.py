import streamlit as st
import requests
st.set_page_config(page_title='Math Routing Agent', layout='wide')

st.markdown('# Math Routing Agent')
st.write('Ask mathematical questions and get step-by-step solutions with AI-powered routing')

question = st.text_area('Enter your math question:', height=120)

if st.button('Get Solution'):
    if not question.strip():
        st.warning('Please enter a question.')
    else:
        with st.spinner('Generating solution...'):
            try:
                resp = requests.post('http://localhost:8000/query', json={'question': question}, timeout=30)
                if resp.status_code == 200:
                    result = resp.json()
                    st.success("Solution generated!")

                    st.markdown("### Question:")
                    st.write(question)

                    st.markdown("### Solution:")

                    # Add a big square box-style container for the solution
                    st.markdown(
                        f"""
                        <div style="
                            background-color:#f9f9f9;
                            border:1px solid #ccc;
                            border-radius:10px;
                            padding:20px;
                            margin-top:10px;
                            width:100%;
                            min-height:300px;
                            font-family:monospace;
                            overflow-wrap: break-word;
                        ">
                            {result['solution']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.caption("Source: Tavily + SerpAPI")

                    # Display web hits if available
                    if result.get('source') == 'web' and result.get('web_hits'):
                        st.markdown("### Sources:")
                        for hit in result['web_hits']:
                            st.markdown(f"- **{hit.get('title', 'No title')}**: {hit.get('snippet', 'No snippet')} ([Link]({hit.get('link', '#')}))")

                    # Feedback loop
                    st.markdown("### Feedback")
                    feedback = st.selectbox("How was the solution?", ["Excellent", "Good", "Average", "Poor"], key="feedback_rating")
                    feedback_comment = st.text_area("Additional comments (optional):", height=80, key="feedback_comment")
                    if st.button("Submit Feedback"):
                        try:
                            feedback_resp = requests.post('http://localhost:8000/feedback', json={
                                'question': question,
                                'rating': feedback,
                                'comment': feedback_comment
                            }, timeout=10)
                            if feedback_resp.status_code == 200:
                                st.success("Thank you for your feedback!")
                            else:
                                st.error(f"Failed to submit feedback: {feedback_resp.text}")
                        except Exception as e:
                            st.error(f"Error submitting feedback: {str(e)}")
                else:
                    st.error(f'Error: {resp.status_code} - {resp.text}')
            except Exception as e:
                st.error('Backend error: ' + str(e))
