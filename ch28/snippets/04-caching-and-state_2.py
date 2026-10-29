if "notes" not in st.session_state:
    st.session_state.notes = []
note = st.text_input("Add a note")
if st.button("Save") and note:
    st.session_state.notes.append(note)
st.write(st.session_state.notes)
