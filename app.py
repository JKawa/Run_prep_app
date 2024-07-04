import streamlit as st
from src.main import weatherPrep
from src.api_ask import OpenIAmessage
import datetime
import re

result = None

def main():
    st.title("Weather App for Runners")
    st.header("Add data")

    chosen_date = st.date_input("Date")
    chosen_hour = st.time_input(label="Time", value=datetime.time(1, 0), step=3600)

    options = ["Wrocław", "Kraków", "Warszawa"]
    choosen_location = st.selectbox(label="Location", options=options)
    training = st.text_input("Describe your training")

    if st.button(label="Prepare tips"):
        click(chosen_date, chosen_hour, choosen_location, training)


def click(date, time, location, training):
    hour = time.hour
    try:
        app = weatherPrep(day=date, city=location)
        app.run()
        result = app.result
        result = _prepare_dataframe(result, hour)
        user_message = f"Using dataframe: {result.to_json} about weather and information about training: {training} describe weather and tell me what can I wear for my running training.Please make your answer to look like: 1:one sentence about weather ; 2: list of clothes separated by coma write only clothes in list [] ; 3: one sentence  with additional advices (do not write here about weather and clothes).  "
        message_instance = OpenIAmessage(user_message)
        message_instance.generate_response()
        segments = re.split(r"(\d+:)", message_instance.answer)

        result_dict = {}

        for i in range(1, len(segments), 2):
            key = int(segments[i][:-1])
            value = segments[i + 1].strip()
            result_dict[key] = value

        st.header("Weather:")
        st.text(result_dict[1])
        st.header(f"Clothes:")
        for el in _prepare_list_from_str(result_dict[2]):
            st.text(f"       - {el}")
        st.header("Tips:")
        st.text(result_dict[3])

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


def _prepare_list_from_str(input):
    input = input.replace("[", "")
    input = input.replace("]", "")
    return input.split(",")


if __name__ == "__main__":
    main()
