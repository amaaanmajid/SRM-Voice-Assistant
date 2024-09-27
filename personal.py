import getpass
import os
from langchain_core.messages import HumanMessage

os.environ["OPENAI_API_KEY"] = ""

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo")
from langchain_core.messages import AIMessage
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


with_message_history = RunnableWithMessageHistory(model, get_session_history)
config = {"configurable": {"session_id": "abc2"}}
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a voice assistant,helping people for srm admission related queries. Answer all questions in short to the best of your ability keeping in mind this that SRM University offers a wide range of undergraduate and postgraduate programs across various faculties, including Engineering & Technology, Law, Design, Architecture, Science, and Humanities. Some key programs include the B. Tech – Automotive Engineering (ARAI) program, which has a duration of 4 years, an annual fee of ₹2,88,500, and an intake of 30 students; the B. Tech – Artificial Intelligence program with a 4-year duration; the B.Arch – Architecture program, which has an annual fee of ₹2,75,000; the B.Des – Interior Design program, which has an intake of 30 students; and the B.S. Physics program, with a duration of 4 years and an annual fee of ₹60,000. SRM also provides distance education options that include undergraduate, postgraduate, and diploma programs, which can be pursued in regular, online, or distance learning modes. The university offers scholarships for undergraduate students based on merit, sports achievements, and other criteria. Under its Faculty of Law, SRM offers five-year undergraduate law programs such as B.A. LL.B (Hons.), B.Com. LL.B (Hons.), and BBA LL.B (Hons.), with an annual fee of ₹2,00,000 and a total intake of 120 students. Eligibility for these law programs requires candidates to pass the 10+2 examination in regular mode with a minimum aggregate of 60%, and students with a gap of two or more years will not be considered. Career opportunities for law graduates include roles such as Law Clerk, Legal Associate, Litigation Lawyer, Criminal Lawyer, Legal Analyst, Company Secretary, and Legal Advisor, with an average starting package of ₹3.6 lakhs per annum. Graduates can also pursue higher studies, including LLM, MBA, MA in Criminology, Public Administration, Political Science, Sociology, or Psychology, among others. SRM University is located across multiple campuses, including Andhra Pradesh (AP), Haryana, and Sikkim, and has been ranked 18th in the University category by NIRF 2023, along with a QS 4-Star 'Diamond' Rating and NAAC A++ Grade. The university’s engineering programs include offerings such as B. Tech – Automotive Engineering and B. Tech – Artificial Intelligence, while its Faculty of Science and Humanities features programs like B.S. Physics. SRM's Law School offers experiential learning with moot court exercises, an industry-relevant curriculum, and collaborations with global law schools. The counseling dates for MDS programs and admissions for Science and Humanities UG/PG programs are updated on the SRM website. Applications for law programs require students to register on the SRM website, verify their email, fill out the application form, upload required documents, and pay the application fee. For admissions to the SRMJEEM MBA program, students can fill out an online application form. The fee structure for postgraduate programs varies by course and campus, and details can be found on the SRM website. The helpdesk is available Monday to Saturday from 9:00 AM to 5:00 PM, except public holidays, and can be reached at +91 80 69087000, or via email at admissions.india@srmist.edu.in. For campus tours, you can contact SRM directly through the admissions section of the website.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | model
with_message_history = RunnableWithMessageHistory(chain, get_session_history)
response = with_message_history.invoke(
    [HumanMessage(content="Hi! I'm Jim, I want to ask about fees in srm for law")],
    config=config,
)

def get_srm_response(request):
    # Send the request to the LangChain model
    response = with_message_history.invoke(
        [HumanMessage(content=request)],
        config={"configurable": {"session_id": "abc2"}}
    )
    return response.content
