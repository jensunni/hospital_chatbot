import uuid # uuid stands for Universally Unique Identifier.
# It is a 128-bit number used in computer systems to uniquely identify information 
# without needing a central database or authority to coordinate it.
import streamlit as st   
# turn data scripts into shareable web apps in minutes
from bot import handle, log, set_feedback

st.set_page_config(page_title="City Hospital Assistant", page_icon="🏥")
st.title("🏥 City Hospital Assistant 🏥")
st.caption("I can book appointments and answer questions about timings, fees and departments. "
           "I cannot give medical advice. For emergencies call 112.")

ss = st.session_state
ss.setdefault("s", {"flow": None})
ss.setdefault("sid", uuid.uuid4().hex[:8])
ss.setdefault("chat", [("bot", "Hello! How can I help you today?", None)])

for i, (who, msg, mid) in enumerate(ss.chat):
    with st.chat_message("assistant" if who == "bot" else "user"):
        st.markdown(msg)
        if who == "bot" and mid and i == len(ss.chat) - 1:
            c1, c2, _ = st.columns([1, 1, 8])
            if c1.button("👍", key=f"up{mid}"): set_feedback(mid, 1); st.toast("Thanks for the feedback!")
            if c2.button("👎", key=f"dn{mid}"): set_feedback(mid, 0); st.toast("Thanks, we'll improve.")

if text := st.chat_input("Type your message..."):
    reply, tag, conf = handle(text, ss.s)
    mid = log(ss.sid, text, reply, tag, conf)
    ss.chat += [("user", text, None), ("bot", reply, mid)]
    st.rerun()