import streamlit as st
from backend import generate_questions_langchain


def main():
    # UI setup
    st.title("Quizzlet")
    st.write("The quiz is generated based on topic")
    left_columns, right_columns = st.columns((3, 1))
    with left_columns:
        topic = st.text_input("Enter the topic of the quizz")
    with right_columns:
        # Get input from user
        number_of_questions = st.number_input(label="Enter number of questions", min_value=1, max_value=10, value=5)

    # store quiz in the state
    if "quizz" not in st.session_state:
        st.session_state.quizz = None

    # Generate questions on click Generate quizz
    if st.button("Generate quizz") and topic and len(topic.strip()) >= 2:
        st.session_state.quizz = generate_questions_langchain(topic=topic, number_of_questions=number_of_questions)

    # If quiz is not empty then render questions
    if st.session_state.quizz is not None:
        questions = st.session_state.quizz["questions"]
        selected_options = []
        for i in range(len(questions)):
            question = questions[i]
            st.write(f"**Question {i + 1}:** {question['question']}")
            selected_option = st.radio("Options: ", question["choices"], key=f"radio_{i}")
            selected_options.append(selected_option)

        st.session_state.selected_options = selected_options
        # on click submit, check score and render correct answers
        if st.button("Submit"):
            correct_answers = 0
            questions = st.session_state.quizz["questions"]
            for i in range(len(questions)):
                question = questions[i]
                select_option = st.session_state.selected_options[i]
                if select_option == question["answer"]:
                    correct_answers = correct_answers + 1
            # score calculation
            total_questions = len(questions)
            score = correct_answers / total_questions * 100
            st.write(f"Score: {score:.2f}%")

            # Render correct answers
            st.write("---")
            st.title("Correct answers")
            for i in range(len(questions)):
                question = questions[i]
                st.write(f"**Question {i + 1}:** {question['question']}")
                st.write(f"**Correct Answer:** {question['answer']}")
                st.write("\n")


if __name__ == '__main__':
    main()
