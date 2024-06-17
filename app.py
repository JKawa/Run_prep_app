import streamlit as st
from src.main import weatherPrep

def main():
    st.title('Streamlit and Selenium Integration !!!')
    st.header("start")
    app = weatherPrep()
    app.run()
    st.header(app.dateToUrl)
    print(app.result)
    st.dataframe(data=app.result)
    st.header("finish")
if __name__ == '__main__':
    main()