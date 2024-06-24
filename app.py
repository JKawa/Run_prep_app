import streamlit as st
from src.main import weatherPrep
from src.api_ask import OpenIAmessage
import datetime

# Global result variable
result = None


def main():
    st.title("Weather App for Runners")

    st.header("Start")

    choosen_date = st.date_input("Add date")
    choosen_hour = st.time_input(label="Add hour", value=datetime.time(1, 0), step=3600)

    options = ["Wrocław", "Kraków", "Warszawa"]
    choosen_location = st.selectbox(label="Add location", options=options)
    st.header(
        f"Date: {choosen_date}, time: {choosen_hour},location: {choosen_location} "
    )

    if st.button(label="Start"):
        click(choosen_date, choosen_hour, choosen_location)

    st.header("Finish")


def click(date, time, location):
    if not date or not time or not location:
        st.error("Please provide a valid date, time, and location.")
        return

    hour = time.hour
    try:
        app = weatherPrep(day=date, city=location)
        app.run()
        result = app.result
        result = _prepare_dataframe(result, hour)
        st.dataframe(data=result)
        user_message = f"Using dataframe: {result.to_json} describe weather and tell me what can I wear for my running training "
        message_instance = OpenIAmessage(user_message)
        message_instance.generate_response()
        st.text(message_instance.answer)

    except Exception as e:
        st.error(f"An error occurred: {e}")


def _prepare_dataframe(dataframe, hour):
    dataframe[["time_1", "time_2"]] = dataframe["Time"].str.split(" ", expand=True)
    dataframe[["time_1a", "time_1b"]] = dataframe["time_1"].str.split(":", expand=True)
    dataframe["time_1a"] = dataframe["time_1a"].astype(int)
    dataframe["time_1a"] = dataframe.apply(
        lambda row: row["time_1a"] + 12
        if row["time_2"] == "pm" and row["time_1a"] != 12
        else (0 if row["time_2"] == "am" and row["time_1a"] == 12 else row["time_1a"]),
        axis=1,
    )

    dataframe = dataframe[dataframe["time_1a"] == hour]
    return dataframe


if __name__ == "__main__":
    main()
